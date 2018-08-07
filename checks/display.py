# Use display_results function for options display!

from termcolor import colored

# Colored output for windows
import colorama
colorama.init()

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
                # Output to *.txt file
                # filename.write('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'red')+']\n'))
                # filename.write('{0:30} * {1:1}'.format(' ', dictionary[key][2]+'\n'))

                # Output to *.html file
                # filename.write('<tr><td>' + ' - '+full_name + key + '</td>' + '<td>[<font color="red">'+dictionary[key][1]+']' + '</font></td></tr>\n')
                # filename.write('<tr><td></td>' + '<td>*'+dictionary[key][2]+'</td></tr>\n')

                # Output best practice to console
                # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))

            elif dictionary[key][0] == 1:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'yellow')+']'))
                # Output to *.txt file
                # filename.write('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'yellow')+']\n'))
                # filename.write('{0:30} * {1:1}'.format(' ', dictionary[key][2]+'\n'))

                # Output to *.html file
                # filename.write('<tr><td>' + ' - '+full_name + key + '</td>' + '<td>[<font color="orange">'+dictionary[key][1]+']' + '</font></td></tr>\n')
                # filename.write('<tr><td></td>' + '<td>*'+dictionary[key][2]+'</td></tr>\n')

                # Output best practice to console
                # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))

            elif dictionary[key][0] == 2:
                print('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'green')+']'))
                # Output to *.txt file
                # filename.write('{0:30} {1:1}'.format(' - '+full_name + key, '['+colored(dictionary[key][1],'green')+']\n'))

                # Output to *.html file
                # filename.write('<tr><td>' + ' - '+full_name + key + '</td>' + '<td>[<font color="green">'+dictionary[key][1]+']' + '</font></td></tr>\n')

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
    # with open(filename + ".html", 'w') as fname:
    # make 1 tab to next uncommented lines, uncomment the line above and next commented lines to write results in file
#         fname.write(
# '''<!doctype html>
# <html>
# <head>
# </head>
# <body>
# <table>
# ''')
    for key in dictionary:
        full_name = ''
        print('\n',colored(key,'blue'))
            # Output to *.txt file
            # fname.write(colored(key, 'blue') + '\n')
            # Output to *.html file
            # fname.write('<tr><td><font color="blue">'+key+'</font></td></tr>\n')

        display_options(dictionary[key],full_name)#, fname)
            # fname.write('<tr><td>&nbsp;</td></tr>\n')
#         fname.write(
# '''</table>
# </body>
# </html>
# ''')

