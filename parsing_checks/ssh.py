# Parse SSH options
# Input:
#       line with ssh option
#           ip ssh time-out 30
# Output:
#       ssh option dictionary
#           {'time-out': '30'}
from pyparsing import Word,alphas,White,restOfLine


def _globalParse___ssh_attributes(line):
    ssh_dict = {}

    ssh_option = (Word(alphas + '-'))('option')
    ssh_value  = (restOfLine)        ('value')

    result     = (ssh_option + White() + ssh_value).parseString(line)

    if   result.option == 'logging':
        ssh_dict['logging-events']         = 'yes'
    elif result.option == 'authentication-retries':
        ssh_dict['authentication_retries'] = result.value.split()[0]
    elif result.option == 'port':
        ssh_dict['port_rotary']            = result.value.split()[0]
    elif result.option == 'maxstartups':
        ssh_dict['maxstartups']            = result.value.split()[0]
    elif result.option == 'time-out':
        ssh_dict['time-out']               = result.value.split()[0]
    elif result.option == 'version':
        ssh_dict['version']                = result.value.split()[0]

    return ssh_dict
