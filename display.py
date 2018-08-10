# Use display_results function for options display!

# Colored output for windows
import colorama
colorama.init()

# Options display
# INPUT:  result dictionary of 1 section, option full name
# SAMPLE: {'dhcp_snooping': {'active': [0, 'DISABLED', 'Turn it off to prevent spoofing attack']}}
# OUTPUT: display colored options with its status
# SAMPLE: - dhcp_snooping active        [DISABLED]
class bcolors:
    BLUE   = '\033[1;34m'
    GREEN  = '\033[1;32m'
    YELLOW = '\033[1;33m'
    RED    = '\033[1;31m'
    END    = '\033[0m'


def display_options(dictionary, full_name, html):
    color = ''
    htmlclr = ''
    for key in dictionary:
        # color assigning based on severity
        if type(dictionary[key]) is list:
            if dictionary[key][0]   == 0:
                color   = bcolors.RED
                htmlclr = 'red'
            elif dictionary[key][0] == 1:
                color   = bcolors.YELLOW
                htmlclr = '#ff7f00'
            elif dictionary[key][0] == 2:
                color   = bcolors.GREEN
                htmlclr = 'green'
            # print value
            print('{0:30} {1:1}'.format(' - '+full_name + key, '['+(color+dictionary[key][1]+bcolors.END)+']'))
            # writing to html
            if html:
                html.write('<tr><td>' + ' - '+full_name + key + '</td>' + '<td style="font-weight: bold; color: '+htmlclr+';">['+dictionary[key][1]+ ']</td></tr>\n')
                try:
                    html.write('<tr><td></td>' + '<td>*'+dictionary[key][2]+'</td></tr>\n')
                except IndexError:
                    pass

            # Output best practice to console
            # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))
        else:
            # go deeper in dictionary structure
            full_name += key + ' '
            display_options(dictionary[key],full_name,html)
            full_name = ''

# Results display
# INPUT:  result dictionary
# SAMPLE: {'ip':{...}, 'active_service': {...},...}
# OUTPUT: colored separated options display
# SAMPLE: ip
#          - dhcp_snooping active        [DISABLED]
def display_results(dictionary,html_file):
    if html_file:
        with open(html_file,'w') as html:
            html.write('<!doctype html>\n<html>\n<head>\n</head>\n<body>\n<table>')
            for key in dictionary:
                full_name = ''
                print('\n', bcolors.BLUE + key + bcolors.END)
                # Output to *.html file
                html.write('<tr><td><font color="blue">' + key + '</font></td></tr>\n')

                display_options(dictionary[key], full_name, html)

                html.write('<tr><td>&nbsp;</td></tr>\n')
            html.write('</table>\n</body>\n</html>')

    else:
        for key in dictionary:
            full_name = ''
            print('\n', bcolors.BLUE + key + bcolors.END)
            display_options(dictionary[key], full_name, html_file)

    # for key in dictionary:
    #     full_name = ''
    #     print('\n', colored(key, 'blue'))
    #     # Output to *.html file
    #     file.write('<tr><td><font color="blue">' + key + '</font></td></tr>\n')
    #
    #     display_options(dictionary[key], full_name)  # , file)
    #
    #
    #
    #
    # # Creating .html files
    # with open(filename + '.html', 'w') as file:
    #
    #     # make 1 tab to all next lines, uncomment the line above and next commented lines to write results in file
    #
    #     file.write('<!doctype html>\n<html>\n<head>\n</head>\n<body>\n<table>')
    #     for key in dictionary:
    #         # dictionary[key] shouldnt be empty, we are writing info into it anyway...
    #         if (dictionary[key] == {}) or (dictionary[key] == []):
    #             continue
    #         full_name = ''
    #         print('\n', colored(key, 'blue'))
    #         # Output to *.html file
    #         file.write('<tr><td><font color="blue">' + key + '</font></td></tr>\n')
    #
    #         display_options(dictionary[key], full_name)  # , file)
    #         file.write('<tr><td>&nbsp;</td></tr>\n')
    #     file.write('</table>\n</body>\n</html>')

