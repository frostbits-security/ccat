# Services options check
# Input:
#        global dictionary with defined 'active_service' and 'disable_service' keys inside it
# Output:
#        services dictionary
def check(global_params):
# create new 'Services' section for further display
    results_dict = {'Services':{}}


# 'should be enable' services section
    if 'password-encryption' in global_params['active_service']:
        results_dict['Services']['password encryption'] = [2, 'ENABLED']
    else:
        results_dict['Services']['password encryption'] = [0, 'DISABLED', 'Turn it on to encrypt passwords']

    if 'tcp-keepalives-in'  in global_params['active_service']:
        results_dict['Services']['tcp keepalives in']   = [2, 'ENABLED']
    else:
        results_dict['Services']['tcp keepalives in']   = [1, 'DISABLED', 'You may need it to prevent stuck sessions']

    if 'tcp-keepalives-out' in global_params['active_service']:
        results_dict['Services']['tcp keepalives out']  = [2, 'ENABLED']
    else:
        results_dict['Services']['tcp keepalives out']  = [1, 'DISABLED', 'You may need it to prevent stuck sessions']


# 'should be disable' services section
    if 'pad'                in global_params['disable_service']:
        results_dict['Services']['pad']               = [2, 'DISABLED']
    else:
        results_dict['Services']['pad']               = [0, 'ENABLED', 'Turn it off to prevent potential unauthorized access']

    if 'config'             in global_params['active_service']:
        results_dict['Services']['config']            = [0, 'ENABLED', 'Turn it off to prevent autoloading configuration file from a network server']
    else:
        results_dict['Services']['config']            = [2, 'DISABLED']

    if   'udp-small-servers' in global_params['active_service']:
        results_dict['Services']['udp small servers'] = [0, 'ENABLED', 'Turn it off to prevent potential information leak and DOS attack']
    elif 'udp-small-servers' in global_params['disable_service']:
        results_dict['Services']['udp small servers'] = [2, 'DISABLED']

    if   'tcp-small-servers' in global_params['active_service']:
        results_dict['Services']['tcp small servers'] = [0, 'ENABLED', 'Turn it off to prevent potential information leak and DOS attack']
    elif 'tcp-small-servers' in global_params['disable_service']:
        results_dict['Services']['tcp small servers'] = [2, 'DISABLED']


    # version dependent services
    if 'version' in global_params:
        version_major, version_minor, version_build = global_params['version'].partition('.')
        version = version_major + version_minor + version_build.replace('.', '')

        if float(version) < 12.1:
            if 'finger' in global_params['disable_service']:
                results_dict['Services']['finger']        = [2, 'DISABLED']
            else:
                results_dict['Services']['finger']        = [0, 'ENABLED', 'Disable it to prevent user to view other active users']

        if float(version) >= 12.2:
            if 'vstack' in global_params['disable_service']:
                results_dict['Services']['smart install'] = [2, 'DISABLED']
            else:
                results_dict['Services']['smart install'] = [0, 'ENABLED', 'Turn it off or block 4786 port (if "vstack" option unavailable) to disable smart install configuration']

        # TCP and UDP small services are enabled by default on Cisco IOS software Release 11.2 and earlier. These commands
        # are disabled by default on Cisco IOS software Software Versions 11.3 and later.
        if 'udp small servers' not in results_dict['Services'] and float(version) <= 11.2:
            results_dict['Services']['udp small servers'] = [0, 'ENABLED', 'Turn it off to prevent potential information leak and DOS attack']
        else:
            results_dict['Services']['udp small servers'] = [2, 'DISABLED']

        if 'tcp small servers' not in results_dict['Services'] and float(version) <= 11.2:
            results_dict['Services']['tcp small servers'] = [0, 'ENABLED', 'Turn it off to prevent potential information leak and DOS attack']
        else:
            results_dict['Services']['tcp small servers'] = [2, 'DISABLED']


    return results_dict
