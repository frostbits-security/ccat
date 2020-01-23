# SSH and global IP options check
# Input:
#        global dictionary with defined 'ip' key inside it
# Output:
#        ssh, ip services and web server options dictionary
def check(global_params):
# create new 'IP options' section for further display
    results_dict = {'IP options':{'SSH':{},'service':{}, 'WEB server':{}}}


# ssh section
    if 'version'                in global_params['ip']['ssh']:
        if global_params['ip']['ssh']['version'] == '2':
            results_dict['IP options']['SSH']['version']                = [2, '2']
        else:
            results_dict['IP options']['SSH']['version']                = [0, '1', 'Turn on SSH 2 mode only to secure you connection']
    else:
        results_dict    ['IP options']['SSH']['version']                = [1, 'BOTH', 'Not SSH version 2 mode only, you may want to turn this mode on']

    if 'authentication_retries' in global_params['ip']['ssh']:
        if int(global_params['ip']['ssh']['authentication_retries']) > 5:
            results_dict['IP options']['SSH']['authentication retries'] = [1, str(global_params['ip']['ssh']['authentication_retries']), 'You may want to decrease it']
        else:
            results_dict['IP options']['SSH']['authentication retries'] = [2, str(global_params['ip']['ssh']['authentication_retries'])]

    if 'time-out'               in global_params['ip']['ssh']:
        if         int(global_params['ip']['ssh']['time-out']) < 100:
            results_dict['IP options']['SSH']['time-out']               = [2, str(global_params['ip']['ssh']['time-out'])]
        elif 100 < int(global_params['ip']['ssh']['time-out']) <= 300:
            results_dict['IP options']['SSH']['time-out']               = [1, str(global_params['ip']['ssh']['time-out']), 'You may want to decrease it']
        elif       int(global_params['ip']['ssh']['time-out']) > 300:
            results_dict['IP options']['SSH']['time-out']               = [0, str(global_params['ip']['ssh']['time-out']), 'Decrease it due to security reasons']

    if 'maxstartups'            in global_params['ip']['ssh']:
        if int(global_params['ip']['ssh']['maxstartups']) < 5:
            results_dict['IP options']['SSH']['max startups']           = [2, str(global_params['ip']['ssh']['maxstartups'])]
        else:
            results_dict['IP options']['SSH']['max startups']           = [1, str(global_params['ip']['ssh']['maxstartups']), 'You may want to decrease it']


# ip services section
    if 'identd'       in global_params['ip']['active_service']:
        results_dict['IP options']['service']['identd']       = [0, 'ENABLED', 'Disable it to prevent user connection information leaks']
    else:
        results_dict['IP options']['service']['identd']       = [2, 'DISABLED']

    if 'source-route' in global_params['ip']['active_service']:
        results_dict['IP options']['service']['source-route'] = [0, 'ENABLED', 'Disable it to prevent packet route leak']
    else:
        results_dict['IP options']['service']['source-route'] = [2, 'DISABLED']

    if 'bootp server' in global_params['ip']['active_service']:
        results_dict['IP options']['service']['bootp server'] = [0, 'ENABLED', 'Disable it to prevent possible IOS image stealing']
    else:
        results_dict['IP options']['service']['bootp server'] = [2, 'DISABLED']

    # version dependent services
    if 'version' in global_params:
        version_major, version_minor, version_build = global_params['version'].partition('.')
        version = version_major + version_minor + version_build.replace('.', '')
        if float(version) >= 12.1:
            if 'finger'   in global_params['ip']['active_service']:
                results_dict['IP options']['service']['finger']   = [0, 'ENABLED', 'Disable it to prevent user to view other active users']
            else:
                results_dict['IP options']['service']['finger']   = [2, 'DISABLED']


# web server section
    if 'type' in global_params['ip']['http']:
        if global_params['ip']['http']['type'] == 'http':
            results_dict['IP options']['WEB server']['type'] = [0, 'HTTP', 'Disable it to prevent insecure connection. You may turn on secure server with "ip http secure-server" command']
        else:
            results_dict['IP options']['WEB server']['type'] = [2, 'HTTPS']
    else:
        results_dict    ['IP options']['WEB server']['type'] = [2, 'DISABLED']

    # "if web server enabled" section
    if results_dict['IP options']['WEB server']['type'][1] is not 'DISABLED':
        if 'max_connections' in global_params['ip']['http']:
            if int(global_params['ip']['http']['max_connections']) > 10:
                results_dict['IP options']['WEB server']['max connections'] = [1, str(global_params['ip']['http']['max_connections']),
                                                                                    'You may want to decrease it due to security reasons']
            else:
                results_dict['IP options']['WEB server']['max connections'] = [2, str(global_params['ip']['http']['max_connections'])]

        if 'port'            in global_params['ip']['http']:
            results_dict    ['IP options']['WEB server']['port']            = [2, str(global_params['ip']['http']['port'])]
        else:
            results_dict    ['IP options']['WEB server']['port']            = [1, 'Default', 'You may want to change it due to security reasons']


    return results_dict
