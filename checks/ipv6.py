import util



##########################
# Global checks
def sourceguard_global(global_params, result_dict):
	return _check_global(global_params, result_dict, 'source guard', 'source-guard', 'Turn it on to prevent spoofing attack')

def dhcpguard_global(global_params, result_dict):
	return _check_global(global_params, result_dict, 'DHCP guard', 'dhcp-guard', 'Turn it on to prevent spoofing attack')

def destinationguard_global(global_params, result_dict):
	return _check_global(global_params, result_dict, 'destination guard', 'destination-guard', 'Turn it on to prevent spoofing attack')

def raguard_global(global_params, result_dict):
	return _check_global(global_params, result_dict, 'RA guard', 'raguard', 'Turn it on to prevent spoofing attack')

def snooping_global(global_params, result_dict):
	return _check_global(global_params, result_dict, 'snooping', 'snooping', 'Turn it on to prevent spoofing attack')

# TODO: description
def _check_global(global_params, result_dict, dispname, indexname, offmessage):
	enabled = 0
	snooping_vlans = []
	result_dict['IPv6 options'][dispname] = {}

	# globals
	try:
		if (global_params['ipv6'][indexname]):
			enabled = 1
			result_dict['IPv6 options'][dispname] = [2, 'ENABLED']
	except:
		result_dict['IPv6 options'][dispname] = [0, 'DISABLED', offmessage]
	return result_dict, enabled

##########################
# Interface checks

# TODO: description
def _check_iface(iface_params, vlanmap_type, allinterf, enabled, dispname, indexname, offmessage):
	result_dict = {}
	if enabled or allinterf:
		try:
			if (iface_params['ipv6'][indexname]):
				enabled = 1
				result_dict[dispname] = [2, 'ENABLED']
		except:
			result_dict[dispname] = [0, 'DISABLED', offmessage]
	return result_dict

def sourceguard_iface(iface_params, vlanmap_type, allinterf, enabled):
	return _check_iface(iface_params, vlanmap_type, allinterf, enabled, 'source guard', 'source-guard', 'Turn it on to prevent spoofing attack')

def dhcpguard_iface(iface_params, vlanmap_type, allinterf, enabled):
	return _check_iface(iface_params, vlanmap_type, allinterf, enabled, 'DHCP guard', 'dhcp-guard', 'Turn it on to prevent spoofing attack')

def destinationguard_iface(iface_params, vlanmap_type, allinterf, enabled):
	return _check_iface(iface_params, vlanmap_type, allinterf, enabled, 'destination guard', 'destination-guard', 'Turn it on to prevent spoofing attack')

def raguard_iface(iface_params, vlanmap_type, allinterf, enabled):
	return _check_iface(iface_params, vlanmap_type, allinterf, enabled, 'RA guard', 'ra-guard', 'Turn it on to prevent spoofing attack')
