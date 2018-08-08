import util
from termcolor import colored
from statistics import median

def check(global_params,iface_params,vlanmap,allinterf,result_dict):
	enabled=0
	snooping_vlans=[]

	# globals
	if(global_params['ip']['dhcp_snooping']['active']=='yes'):
		enabled=1
		result_dict['ip']['dhcp_snooping']['active'] = [2,'ENABLED']
		if ('vlans' in global_params['ip']['dhcp_snooping']):
			snooping_vlans=util.intify(global_params['ip']['dhcp_snooping']['vlans'])
	else:
		result_dict['ip']['dhcp_snooping']['active'] = [0,'DISABLED', 'Turn it on to prevent spoofing attack']

	# ifaces
	if(enabled):
		for i in iface_params:
			try:
				iface_snoop=iface_params[i]['dhcp_snoop']
			except:
				continue
			iface_vlans=[]
			if 'vlans' in iface_params[i]:
				iface_vlans=iface_params[i]['vlans']
			if (not (allinterf) and iface_params[i]['shutdown']=='yes'):
				continue
			else:
				mode=iface_snoop['mode']
				if(mode=='untrust'):

					if 'limit' in iface_snoop:
						chkres=0
						try:
							chkres=int(iface_snoop['limit'])>100
						except:
							chkres=int(iface_snoop['limit'].split(' ')[0])>100
						if(chkres):
							result_dict['ip']['dhcp_snooping']['limit'] = [0, 'Too high level at interface '+i]
					else:
						result_dict['ip']['dhcp_snooping']['limit'] = [0, 'No DHCP snooping rate at interface ' + i]

				elif(mode=='trust'):
					if(vlanmap and iface_vlans):
						if(set(vlanmap[2]).isdisjoint(iface_vlans)):
							result_dict['ip']['dhcp_snooping']['vlans'] = [1,'Interface '+i+'set as trusted, but vlanmap is different',
																		   'Check vlans on vlanmap and this interface']
				else:
					print('Unknown mode: '+mode)

	return result_dict