#############################
# ARP inspection check

import util

def check(global_params,iface_params,vlanmap,allinterf,result_dict):
	enabled=0
	snooping_vlans=[]
	result_dict['ip']['ARP inspection']={}
	
	# globals
	if(global_params['ip']['arp_inspection']['active']=='yes'):
		enabled=1
		result_dict['ip']['ARP inspection'] = [2,'ENABLED']
		if ('vlans' in global_params['ip']['arp_inspection']):
			snooping_vlans=util.intify(global_params['ip']['arp_inspection']['vlans'])
	else:
		result_dict['ip']['ARP inspection'] = [0,'DISABLED', 'Turn it on to prevent spoofing attack']


	### Interfaces
	if(enabled):
		for i in iface_params:
			# create dictionary for output
			if not (i in result_dict):
				result_dict[i]={}
			# check if dhcp snooping is active on interface
			try:
				iface_arp=iface_params[i]['arp_insp']
			except:
				continue
			iface_vlans=[]
			# check if interface has vlans on it
			if 'vlans' in iface_params[i]:
				iface_vlans=iface_params[i]['vlans']
			# check if interface is turned off, and if we need to check disabled interfaces
			if (not (allinterf) and iface_params[i]['shutdown']=='yes'):
				continue
			else:
				# create dictionary for output
				if not ('ARP inspection' in result_dict[i]):
					result_dict[i]['ARP inspection']={}
				mode=iface_arp['mode']

				if((mode=='trust') and vlanmap and iface_vlans):
					if(set(vlanmap[2]).isdisjoint(iface_vlans)):
						result_dict[i]['ARP inspection']['vlans'] = [0,'Interface set as trusted, but vlanmap is different','This interface is not trusted according to vlanmap, but marked as trusted. ARP spoofing is possible.']
				else:
					pass
	return result_dict