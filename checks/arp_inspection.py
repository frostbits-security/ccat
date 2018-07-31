import util
from termcolor import colored
from statistics import median

def check(global_params,iface_params,vlanmap,allinterf):
	nabled=0
	snooping_vlans=[]

	# globals
	if(global_params['ip_arp_inspection']['active']=='yes'):
		enabled=1
		if ('vlans' in global_params['ip_arp_inspection']):
			snooping_vlans=util.intify(global_params['ip_arp_inspectionz']['vlans'])
	else:
		print (colored('ARP inspection disabled','red',attrs=['bold']))
		score.append(3)

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
				mode=iface_snoop['mode']
				# dirty hack cuz parsing returns lists sometimes
				if type(mode) is list:
					mode=mode[0]

	return median(score)