import util
from termcolor import colored

def dhcp_snoop(global_params,iface_params,vlanmap,allinterf):
	score=[]
	enabled=0
	snooping_vlans=[]

	# globals
	if(global_params['ip_dhcp_snoop']['active']=='yes'):
		enabled=1
		if ('vlans' in global_params['ip_dhcp_snoop']):
			snooping_vlans=util.intify(global_params['ip_dhcp_snoop']['vlans'])
	else:
		print (colored('DHCP snooping disabled','yellow',attrs=['bold']))
		score.append(2)

	# ifaces
	if(enabled):
		for i in iface_params:
			iface_snoop=iface_params[i]['dhcp_snoop']
			iface_vlans=[]
			if 'vlans' in iface_params[i]:
				iface_vlans=iface_params[i]['vlans']
			if (not (allinterf) and iface_params[i]['shutdown']=='yes'):
				continue
			else:
				continue
				mode=iface_snoop['mode']
				# dirty hack cuz parsing returns lists sometimes
				if type(mode) is list:
					mode=mode[0]
				if(mode=='untrust'):

					if 'limit' in iface_snoop:
						if(int(iface_snoop['limit'][0])>100):
							print (colored('DHCP snooping rate limit is too high','blue',attrs=['bold']))
							score.append(1)
					else:
						print (colored('No DHCP snooping rate limit','blue',attrs=['bold']))
						score.append(1)

				elif(mode=='trust'):
					if(vlanmap and iface_vlans):
						if(set(vlanmap[3]).isdisjoint(iface_vlans)):
							print (colored('Interface '+i+' set as trusted, but vlanmap is different','yellow',attrs=['bold']))
							score.append(2)
				else:
					print('Unknown mode: '+mode)



				print(iface_params[i]['dhcp_snoop'])	

	return util.totalscore(score)

'''
def arp_inspection(global_params,iface_params):
	score=[]
	allinterf=0
	
	if(global_params['ip_arp_inspection']['active']=='yes'):
		pass
	else:
		print (colored("ARP inspection disabled","yellow"))
		score.append(2)

	return util.totalscore(score)
'''