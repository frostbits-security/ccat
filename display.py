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
    BLUE = '\033[1;34m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[1;31m'
    END= '\033[0m'


def display_options(dictionary, full_name,file,outtype):
    for key in dictionary:
        # skip empty dicts
        if (dictionary[key]=={}) or (dictionary[key]==[]):
            continue
        # color assigning based on severity
        if type(dictionary[key]) is list:
            color=''
            htmlclr=''
            if dictionary[key][0] == 0:
                color=bcolors.RED
                htmlclr='red'
            if dictionary[key][0] == 1:
                color=bcolors.YELLOW
                htmlclr='#ff7f00'
            if dictionary[key][0] == 2:
                color=bcolors.GREEN
                htmlclr='green'
            # print value
            print('{0:30} {1:1}'.format(' - '+full_name + key, '['+(color+dictionary[key][1]+bcolors.END)+']'))
            # writing to txt
            if(outtype and outtype=='txt'):
                file.write('{0:30} {1:1}'.format(' - '+full_name + key, '['+dictionary[key][1]+']\n'))
                try:
                    file.write('{0:30} * {1:1}'.format(' ', dictionary[key][2]+'\n'))
                except:
                    pass
            # writing to html
            elif(outtype):
                file.write('<tr><td>' + ' - '+full_name + key + '</td>' + '<td style="font-weight: bold; color: '+htmlclr+';">['+dictionary[key][1]+ ']</td></tr>\n')
                try:
                    file.write('<tr><td></td>' + '<td>*'+dictionary[key][2]+'</td></tr>\n')
                except:
                    pass

            # Output best practice to console
            # print('{0:30} * {1:1}'.format(' ',dictionary[key][2]))
        else:
            # go deeper in dictionary structure
            full_name += key + ' '
            display_options(dictionary[key],full_name,file,outtype)
            full_name = ''

# Results display
# INPUT:  result dictionary
# SAMPLE: {'ip':{...}, 'active_service': {...},...}
# OUTPUT: colored separated options display
# SAMPLE: ip
#          - dhcp_snooping active        [DISABLED]
def display_results(dictionary,file,outtype):
    for key in dictionary:
        # skip empty dicts
        if (dictionary[key]=={}) or (dictionary[key]==[]):
            continue
        full_name = ''
        # print title
        print('\n',(bcolors.BLUE+key+bcolors.END))
        # write to txt
        if(outtype and outtype=='txt'):
            file.write(key)
        # write to html
        elif(outtype):
            file.write('<tr><td><font color="blue">'+key+'</font></td></tr>\n')
        # parse dict
        display_options(dictionary[key],full_name,file,outtype)