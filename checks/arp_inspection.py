import util
from termcolor import colored
from statistics import median

def check(global_params,iface_params,vlanmap,allinterf,result_dict):
	enabled=0
	snooping_vlans=[]

	# globals
	if(global_params['ip']['arp_inspection']['active']=='yes'):
		enabled=1
		result_dict['ip']['arp_inspection']['active'] = [2,'ENABLED']
		if ('vlans' in global_params['ip']['arp_inspection']):
			snooping_vlans=util.intify(global_params['ip']['arp_inspection']['vlans'])
	else:
		# print (colored('ARP inspection disabled','red',attrs=['bold']))
		result_dict['ip']['arp_inspection']['active'] = [0,'DISABLED', 'Turn it on to prevent spoofing attack']
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

	return result_dict