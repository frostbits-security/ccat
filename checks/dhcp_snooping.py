#############################
# DHCP Snooping check

import util
from termcolor import colored
from statistics import median

def check(global_params,iface_params,vlanmap,allinterf,result_dict):
	enabled=0
	snooping_vlans=[]

	### Globals
	# Checking if dhcp snooping is enabled
	if(global_params['ip']['dhcp_snooping']['active']=='yes'):
		enabled=1
		result_dict['ip']['dhcp_snooping']['active'] = [2,'ENABLED']
		if ('vlans' in global_params['ip']['dhcp_snooping']):
			snooping_vlans=util.intify(global_params['ip']['dhcp_snooping']['vlans'])
	else:
		result_dict['ip']['dhcp_snooping']['active'] = [0,'DISABLED', 'Enable this feature to prevent MITM and DHCP starvation attacks']

	### Interfaces
	if(enabled):
		for i in iface_params:
			# create dictionary for output
			if not (i in result_dict):
				result_dict[i]={}
			# check if dhcp snooping is active on interface
			try:
				iface_snoop=iface_params[i]['dhcp_snoop']
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
				if not ('dhcp snooping' in result_dict[i]):
					result_dict[i]['dhcp snooping']={}
				mode=iface_snoop['mode']

				if(mode=='untrust'):
					# check if limit is set and range is good
					if 'limit' in iface_snoop:
						chkres=0
						try:
							chkres=int(iface_snoop['limit'])>100
						# need to handle something like '100 burst 10' 
						except:
							chkres=int(iface_snoop['limit'].split(' ')[0])>100
						if(chkres):
							result_dict[i]['dhcp snooping']['rate limit'] = [1, 'Too high', 'DHCP starvation prevention is inefficient']
					else:
						result_dict[i]['dhcp snooping']['rate limit'] = [1, 'Not set', 'Needed to prevent DHCP starvation']
				# check if trusted interface is marked as trusted in vlamap
				elif((mode=='trust') and vlanmap and iface_vlans):
					if(set(vlanmap[2]).isdisjoint(iface_vlans)):
						result_dict[i]['dhcp snooping']['vlans'] = [0,'Interface set as trusted, but vlanmap is different','This interface is not trusted according to vlanmap, but marked as trusted. Unauthorized DHCP server can work here']
				else:
					pass
	return result_dict