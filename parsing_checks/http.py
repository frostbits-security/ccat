# Parse HTTP options
# Input:
#       line with http option
#           ip http secure-server
# Output:
#       http option dictionary
#           {'type': 'HTTPS'}
def _globalParse___http_attributes(line):
    http_dict = {}

    if   line == 'server':
        http_dict['type']            = 'http'
    elif line == 'secure-server':
        http_dict['type']            = 'https'
    elif line.split()[0] == 'max-connections':
        http_dict['max_connections'] = line.split()[-1]
    elif line.split()[0] == 'port':
        http_dict['port']            = line.split()[-1]

    return http_dict
