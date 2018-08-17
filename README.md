# CCAT
Cisco Config Anaysis Tool

This tool is designed to analyze the configuration files of Cisco devices. In this release only switches are supported. The list of checks is based on the Cisco Guide to Harden Cisco IOS Devices.
A full list of checks is available [here](https://github.com/cisco-config-analysis-tool/ccat/wiki/List-of-the-checks).  
## Usage  

`ccat config_directory -vl vlmap.txt -o result_html_files_directory --storm_level 40.0 --max_number_mac 100  --disabled-interfaces --no-console-display` 

**config_directory** - path to directory with configuration files

**-vl** - path to [vlanmap file](https://github.com/cisco-config-analysis-tool/ccat/wiki/Vlanmap-file)

**-o** - path to output html files directory

**--storm_level** - appropriate level for storm-control (by default value = 80)

**--max_number_mac** - maximum number of mac-addresses for port-security (by default value = 10)

**--disabled-interfaces** - check interfaces even if they are turned off

**--no-console-display** - output analysis results only in html files directory

## Installation  

`pip3 -r requirements.txt`  
`python3 setup.py install`  
