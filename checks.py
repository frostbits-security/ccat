import util
from termcolor import colored

def dhcpsnoop(global_params,iface_params):
	score=[]
	
	if(global_params['ip_dhcp_snoop']['active']=='yes'):
		pass
	else:
		print (colored("DHCP snooping disabled","yellow"))
		score.append(2)

	return util.totalscore(score)

def arpinspection(global_params,iface_params):
	score=[]
	
	if(global_params['ip_arp_inspection']['active']=='yes'):
		pass
	else:
		print (colored("ARP inspection disabled","yellow"))
		score.append(2)

	return util.totalscore(score)