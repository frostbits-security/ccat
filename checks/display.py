# Use display_results function for options display!

from termcolor import colored

# Options display
# INPUT:  result dictionary of 1 section, option full name
# SAMPLE: {'dhcp_snooping': {'active': [0, 'DISABLED', 'Turn it off to prevent spoofing attack']}}
# OUTPUT: display colored options with its status
# SAMPLE: - dhcp_snooping active        [DISABLED]
def display_options(dictionary, full_name):
    for key in dictionary:
        if type(dictionary[key]) is list:
            if dictionary[key][0] == 0:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'red')+']'))
                # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))
            elif dictionary[key][0] == 1:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'yellow')+']'))
                # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))
            elif dictionary[key][0] == 2:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'white')+']'))
        else:
            full_name += key + ' '
            display_options(dictionary[key],full_name)
            full_name = ''

# Results display
# INPUT:  result dictionary
# SAMPLE: {'ip':{...}, 'active_service': {...},...}
# OUTPUT: colored separated options display
# SAMPLE: ip
#          - dhcp_snooping active        [DISABLED]
def display_results(dictionary):
    for key in dictionary:
        full_name = ''
        print('\n',colored(key,'blue'))
        display_options(dictionary[key],full_name)

