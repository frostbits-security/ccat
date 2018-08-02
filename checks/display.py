# Use display_results function for options display!

from termcolor import colored

# Options display
# INPUT:  result dictionary of 1 section, option full name
# SAMPLE: {'dhcp_snooping': {'active': [0, 'DISABLED', 'Turn it off to prevent spoofing attack']}}
# OUTPUT: display colored options with its status
# SAMPLE: - dhcp_snooping active        [DISABLED]
def display_options(dictionary, full_name):#, filename):
    for key in dictionary:
        if type(dictionary[key]) is list:
            if dictionary[key][0] == 0:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'red')+']'))
                # Output to file
                # filename.write('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'red')+']\n'))
                # filename.write('{0:30} * {1:1}'.format(' ', dictionary[key][2]+'\n'))

                # Output best practice to console
                # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))

            elif dictionary[key][0] == 1:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'yellow')+']'))
                # Output to file
                # filename.write('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'yellow')+']\n'))
                # filename.write('{0:30} * {1:1}'.format(' ', dictionary[key][2]+'\n'))

                # Output best practice to console
                # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))

            elif dictionary[key][0] == 2:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'white')+']'))
                # Output to file
                # filename.write('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'white')+']\n'))

        else:
            full_name += key + ' '
            display_options(dictionary[key],full_name)#, filename)
            full_name = ''

# Results display
# INPUT:  result dictionary
# SAMPLE: {'ip':{...}, 'active_service': {...},...}
# OUTPUT: colored separated options display
# SAMPLE: ip
#          - dhcp_snooping active        [DISABLED]
def display_results(dictionary):#, filename):
    # with open(filename + ".txt", 'w') as fname:
    # uncomment the line above and make 1 tab to next lines to write results in file
    for key in dictionary:
        full_name = ''
        print('\n',colored(key,'blue'))
        # fname.write(colored(key, 'blue') + '\n')
        display_options(dictionary[key],full_name)#, fname)

