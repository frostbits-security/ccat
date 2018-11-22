# CCAT
Cisco Config Anaysis Tool

This tool is designed to analyze the configuration files of Cisco devices. The [list of checks](https://github.com/cisco-config-analysis-tool/ccat/wiki/List-of-the-checks) is based on the [Cisco Guide to Harden Cisco IOS Devices](https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html).

## Installation  

`pip3 install -r requirements.txt` 

## Usage  
The simplest way to use:
`python3 ccat.py configuration_file`

Windows:
`ccat.exe configuration_file`

Extended options:

`python3 ccat.py config_directory -vl vlmap.txt -o result_html_files_directory --storm_level 40.0 --max_number_mac 100  --disabled-interfaces --no-console-display --graph network_map` 

**config_directory** - path to directory with configuration files

**-vl** - path to [vlanmap file](https://github.com/cisco-config-analysis-tool/ccat/wiki/Vlanmap-file)

**-o** - path to output html files directory

**--storm_level** - appropriate level for storm-control (by default value = 80)

**--max_number_mac** - maximum number of mac-addresses for port-security (by default value = 10)

**--disabled-interfaces** - check interfaces even if they are turned off

**--no-console-display** - output analysis results in html files directory or into network graph

**--dump-creds** - dump usernames, passwords and hashes from configs
 
**--graph** - builds network map of VLANs (you may left the argument empty to get into interactive mode or define a file name for graph output in png extension)
 
