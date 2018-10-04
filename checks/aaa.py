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
    # Is default list defined?
    flag_default_list = False

    if 'groups' in global_params['aaa']:
        if 'tacacs+' in global_params['aaa']['groups']:
            # for future tasks
            pass

        if 'radius' in global_params['aaa']['groups']:
            # for future tasks
            pass
    if 'authentication' in global_params['aaa']:
        # Check every created authentication login type
        for login_auth in global_params['aaa']['authentication']:
            # Does local or none methods are used in AAA configuration?
            flag_local_or_none = False
    
            # Create named AAA list to result dictionary
            results_dict['AAA'].setdefault('list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"', {})
    
            if 'enable' in global_params['aaa']['authentication'][login_auth]['methods']:
                # start exec password check only if enable method is active
                results_dict.update(checks.exec.check(global_params))
    
            if 'none'   in global_params['aaa']['authentication'][login_auth]['methods']:
                # If "none" method is the Primary method (staying on first position in list)
                if 'none' in global_params['aaa']['authentication'][login_auth]['methods'][0]:
                    results_dict['AAA']['list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"']['method'] = [0,'NONE','Method "none" should not be in authentication methods, especially as primary method, change it to another to prevent insecure behaviour']
                # And its not secure to use "none" method anyway
                else:
                    results_dict['AAA']['list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"']['method'] = [1,'NONE','Method "none" should not be in authentication methods, change it to another method to prevent insecure behaviour']
                flag_local_or_none = True
    
            if 'local'  in global_params['aaa']['authentication'][login_auth]['methods']:
                # "Local-case" method is more secure than "Local"
                results_dict['AAA']['list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"']['method'] = [1, 'LOCAL','Its better to change "Local" method to "Local-case" to make local account is case-sensitive, thus making brute-force attacks less effective']
    
                # start users check only if local method is active
                results_dict.update(checks.users.check(global_params))
                flag_local_or_none = True
    
            if not flag_local_or_none:
                # Is logging enabled?
                find_commands = False
                if 'accounting' in global_params['aaa']:
                    for login_acc in global_params['aaa']['accounting']:
                        if global_params['aaa']['accounting'][login_acc]['login'] == 'commands':
                            # Yes, logging is enabled
                            find_commands = True
                # If logging is disabled
                if not find_commands:
                    results_dict['AAA']['list "' + global_params['aaa']['authentication'][login_auth]['list'] + '"']['logging'] = [1,'DISABLED', 'enable logging to increase authentication security']
    
            # Is "default" method defined?
            if global_params['aaa']['authentication'][login_auth]['list'] == 'default':
                flag_default_list = True
    

    # If "default" method is not defined
    if not flag_default_list:

        # Check every line type
        for line_type in global_params['line']:
            # Does this line use defined list from aaa configuration?
            used_list = False

            # If login method on this line is defined
            if ('login_type' in global_params['line'][line_type]):
                if('authentication' in global_params['aaa']):

                    for login_type in global_params['aaa']['authentication']:

                        # Compare this login method on line with all defined in AAA configuration
                        if global_params['line'][line_type]['login_type'] == global_params['aaa']['authentication'][login_type]:

                            # Yes, this line uses list from aaa configuration
                            used_list = True
                            break

            # If this line does not use list from aaa configuration without defined default list
            if not used_list:
                results_dict['AAA']['line ' + line_type + ' uses AAA list'] = [1, 'NO', 'This line does not use any lists from aaa configuration and default list was not defined']


    return results_dict
