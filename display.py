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
    WHITE  = '\033[1;37m'
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
                color = bcolors.GREEN
                htmlclr = 'green'
            elif dictionary[key][0] == 3:
                color   = bcolors.WHITE
                htmlclr = 'black'
            # Print option and status to console
            print('{0:50} {1:1}'.format(' - '+full_name + key, '['+(color+dictionary[key][1]+bcolors.END)+']'))
            # Print option and status to html file if needed
            if html:
                html.write('<tr><td>' + ' - '+full_name + key + '</td>' + '<td style="font-weight: bold; color: '+htmlclr+';">['+dictionary[key][1]+ ']</td></tr>\n')
                # Try to print 'best practice' to html file
                try:
                    html.write('<tr><td></td>' + '<td>*'+dictionary[key][2]+'</td></tr>\n')
                except IndexError:
                    pass
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
        # Create and open new .html file
        with open(html_file,'w') as html:
            html.write('<!doctype html>\n<html>\n<head>\n</head>\n<body>\n<table>')
            for key in dictionary:
                full_name = ''
                # Print field name to console
                print('\n', bcolors.BLUE + key + bcolors.END)
                # Print field name to html file
                html.write('<tr><td><font color="blue">' + key + '</font></td></tr>\n')

                # Print options in this field
                display_options(dictionary[key], full_name, html)

                html.write('<tr><td>&nbsp;</td></tr>\n')
            # Html file ending
            html.write('</table>\n</body>\n</html>')
    else:
        for key in dictionary:
            full_name = ''
            print('\n', bcolors.BLUE + key + bcolors.END)
            display_options(dictionary[key], full_name, html_file)
