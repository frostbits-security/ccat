# CCAT
Cisco Config Anaysis Tool

This tool is designed to analyze the configuration files of Cisco devices. In this release only switches are supported. The list of checks is based on the Cisco Guide to Harden Cisco IOS Devices.
A full list of checks is in the Wiki.
## Usage  

`ccat -c example -vl vlmap.txt` 

**-c** - path to configuration file

**-vl** - path to [vlanmap file](https://github.com/cisco-config-analysis-tool/ccat/wiki/Vlanmap-file)

## Installation  

`pip3 -r requirements.txt`  
`python3 setup.py install`  
