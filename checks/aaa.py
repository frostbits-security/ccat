# AAA options check
# Input:
#        global dictionary with defined 'aaa' key inside it
# Output:
#        AAA dictionary
import checks
from checks import exec, users

def check(global_params):
# create new 'AAA' section for further display
    results_dict = {'AAA':{}}


    # 1)
    if 'tacacs+' in global_params['aaa']['groups']:
        # for future
        pass

    # 2)
    if 'radius' in global_params['aaa']['groups']:
        # for future
        pass

    # Check every login type in aaa authentication
    for login_auth in global_params['aaa']['authentication']:
        # 7)
        flag_local_or_none = False

        # Create new item for every list name
        results_dict['AAA'].setdefault('list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"', {})

        # 3)
        if 'enable' in global_params['aaa']['authentication'][login_auth]['methods']:
            # start exec password check only if enable method is active
            results_dict.update(checks.exec.check(global_params))

        # 4)
        if 'none' in global_params['aaa']['authentication'][login_auth]['methods']:
            # If "none" method is the Primary method (staying on first position in list)
            if 'none' in global_params['aaa']['authentication'][login_auth]['methods'][0]:
                results_dict['AAA']['list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"']['method'] = [0,'NONE','Method "none" should not be in authentication methods, especially as primary method, change it to another to prevent insecure behaviour']
            else:
                results_dict['AAA']['list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"']['method'] = [1,'NONE','Method "none" should not be in authentication methods, change it to another method to prevent insecure behaviour']
            flag_local_or_none = True

        # 5)
        if 'local' in global_params['aaa']['authentication'][login_auth]['methods']:
            # start users check only if local method is active
            results_dict.update(checks.users.check(global_params))
            flag_local_or_none = True

        # 7)
        if not flag_local_or_none:
            # Is logging is enabled?
            find_commands = False

            for login_acc in global_params['aaa']['accounting']:
                if global_params['aaa']['accounting'][login_acc]['login'] == 'commands':
                    # Yes, logging is enabled
                    find_commands = True
            # If logging is disabled
            if not find_commands:
                results_dict['AAA']['list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"']['logging'] = [1,'DISABLED', 'enable logging to increase authentication security']

    # 8)
    if 'groups' in global_params['aaa']:
        # Check every line type
        for line_type in global_params['line']:
            # Is this line uses group from aaa configuration?
            used_group = False
            if 'login_type' in global_params['line'][line_type]:
                for group_type in global_params['aaa']['groups']:
                    if global_params['line'][line_type]['login_type'] in global_params['aaa']['groups'][group_type]:
                        # Yes, this line uses group from aaa configuration
                        used_group = True
            # If this line doesnt use group from aaa configuration
            if not used_group:
                results_dict['AAA'][line_type+' uses AAA group'] = [1, 'NO', 'its better to use it if it was configured']


    return results_dict
