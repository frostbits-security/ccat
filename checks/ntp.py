# NTP options check
# Input:
#        global dictionary with defined 'ntp_servers'
# Output:
#        NTP dictionary
def check(global_params):
    # create new 'NTP' section for further display
    results_dict = {'NTP': {}}

    if 'ntp_servers' in global_params:
        ntp_count = len(global_params['ntp_servers'])
    else:
        ntp_count = 0

    if ntp_count > 2:
        results_dict['NTP']['Number of NTP servers'] = [
            2, str(ntp_count), 'All good']
    else:
        results_dict['NTP']['Number of NTP servers'] = [
            0, str(ntp_count), 'You need to enable > 3 NTP servers']

    return results_dict
