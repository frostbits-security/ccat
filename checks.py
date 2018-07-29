import util
from termcolor import colored

def dhcp_snoop(global_params,iface_params,allinterf):
	score=[]
	enabled=0

	# globals
	if(global_params['ip_dhcp_snoop']['active']=='yes'):
		enabled=1
	else:
		print (colored("DHCP snooping disabled","red"))
		score.append(2)

	# ifaces
	if(enabled):
		for i in iface_params:
			if (not (allinterf) and iface_params[i]['shutdown']=='yes'):
				continue
			else:
				print(iface_params[i])

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