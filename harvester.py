#!/usr/bin/env python3
####
# Credentials harvesting module
import re
import os

# Legacy code from early stages
"""import sys

try:
	directory=sys.argv[1]+'/'
	filelist=os.listdir(directory)
except:
	print("Usage: ./harvester.py /path/to/dir/with/configs")
	exit()"""

reg_pass=r"enable password (\d).+\b([\w$\\]+)"
reg_secret=r"enable secret (\d).+([\w\$\\]{30,43})"
reg_username_pass=r"username ([\w]+).+password (\d) \b(.+)"
reg_username_secret=r"username ([\w]+).+secret (\d).+([\w\$\\]{30,43})"

usernames=[]
passwords=[]
secrets=[]
clears=[]


def parsepass(content):
	global passwords
	global reg_pass
	res=re.findall(reg_pass,content)
	if(res):
		for result in res:
			passwords.append(result)

def parsesecret(content):
	global secrets
	global reg_secret
	res=re.findall(reg_secret,content)
	if(res):
		for result in res:
			secrets.append(result)

def parseuserpass(content):
	global passwords
	global usernames
	global reg_username_pass
	res=re.findall(reg_username_pass,content)
	if(res):
		for result in res:
			passwords.append(tuple([result[1],result[2]]))
			usernames.append(result[0])			

def parseusersecret(content):
	global secrets
	global usernames
	global reg_username_secret
	res=re.findall(reg_username_secret,content)
	if(res):
		for result in res:
			secrets.append(tuple([result[1],result[2]]))
			usernames.append(result[0])

#### Type 7 decoding
#from https://github.com/theevilbit/ciscot7
xlat = [0x64, 0x73, 0x66, 0x64, 0x3b, 0x6b, 0x66, 0x6f, 0x41, 0x2c, 0x2e, 0x69, 0x79, 0x65, 0x77, 0x72, 0x6b, 0x6c, 0x64
, 0x4a, 0x4b, 0x44, 0x48, 0x53, 0x55, 0x42, 0x73, 0x67, 0x76, 0x63, 0x61, 0x36, 0x39, 0x38, 0x33, 0x34, 0x6e, 0x63,
0x78, 0x76, 0x39, 0x38, 0x37, 0x33, 0x32, 0x35, 0x34, 0x6b, 0x3b, 0x66, 0x67, 0x38, 0x37]
def decrypt_type7(ep):
	"""
	Based on http://pypi.python.org/pypi/cisco_decrypt/
	Regex improved
	"""
	global xlat
	dp = ''
	regex = re.compile('(^[0-9A-Fa-f]{2})([0-9A-Fa-f]+)')
	result = regex.search(ep)
	s, e = int(result.group(1)), result.group(2)
	for pos in range(0, len(e), 2):
		magic = int(e[pos] + e[pos+1], 16)
		if s <= 50:
			# xlat length is 51
			newchar = '%c' % (magic ^ xlat[s])
			s += 1
		if s == 51: s = 0
		dp += newchar
	return dp

def harvest(filelist):
	global reg_pass
	global reg_secret
	global reg_username_pass
	global reg_username_secret
	global usernames
	global passwords
	global secrets
	global clears
	
	for file in filelist:
		with open(file) as infile:
			try:
				tmp=infile.read()
			except:
				continue
			parseusersecret(tmp)
			parseuserpass(tmp)
			parsesecret(tmp)
			parsepass(tmp)
	
	passwords=list(set(passwords))
	for passw in passwords:
		if(passw[0]=="0"):
			clears.append(passw[1])
			continue
		try:	
			clears.append(decrypt_type7(passw[1]))
		except:
			continue
		
	with open('dumped_usernames.txt', 'w') as outfile:
		for username in list(set(usernames)):
			outfile.write("%s\n" % username)
	with open('dumped_passwords.txt', 'w') as outfile:
		for password in list(set(clears)):
			outfile.write("%s\n" % password)
	m500=open('dumped_hashes_m500.txt', 'w')
	m5700=open('dumped_hashes_m5700.txt', 'w')
	for secret in list(set(secrets)):
		if secret[0]=="5":
			m500.write("%s\n" % secret[1])
		elif secret[0]=="4":
			m5700.write("%s\n" % secret[1])
	m500.close()
	m5700.close()