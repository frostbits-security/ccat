import util
from termcolor import colored
from statistics import median

def check(global_params,iface_params,vlanmap,allinterf,result_dict):
	score=[]
	enabled=0
	snooping_vlans=[]

	# globals
	if(global_params['ip']['dhcp_snooping']['active']=='yes'):
		enabled=1
		result_dict['ip']['dhcp_snooping']['active'] = [2,'ENABLED']
		if ('vlans' in global_params['ip']['dhcp_snooping']):
			snooping_vlans=util.intify(global_params['ip']['dhcp_snooping']['vlans'])
	else:
		# print (colored('DHCP snooping disabled','red',attrs=['bold']))
		result_dict['ip']['dhcp_snooping']['active'] = [0,'DISABLED', 'Turn it on to prevent spoofing attack']
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
				if(mode=='untrust'):

					if 'limit' in iface_snoop:
						if(int(iface_snoop['limit'])>100):
							# print (colored('DHCP snooping rate limit is too high at interface '+i,'blue',attrs=['bold']))
							result_dict['ip']['dhcp_snooping']['limit'] = [0, 'Too high level at interface '+i,
																		   'Decrease this level to prevent dhcp attack']
							score.append(1)
					else:
						# print (colored('No DHCP snooping rate limit at interface '+i,'blue',attrs=['bold']))
						result_dict['ip']['dhcp_snooping']['limit'] = [0, 'No DHCP snooping rate at interface ' + i,
																	   'Define this level to prevent dhcp attack']
						score.append(1)

				elif(mode=='trust'):
					if(vlanmap and iface_vlans):
						if(set(vlanmap[2]).isdisjoint(iface_vlans)):
							# print (colored('Interface '+i+' set as trusted, but vlanmap is different','yellow',attrs=['bold']))
							result_dict['ip']['dhcp_snooping']['vlans'] = [1,'Interface '+i+'set as trusted, but vlanmap is different',
																		   'Check vlans on vlanmap and this interface']
							score.append(2)
				else:
					print('Unknown mode: '+mode)

	return median(score), result_dict