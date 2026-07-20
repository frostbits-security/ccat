<h1 align="center">
  <br>
  <img src="./ccat.png" alt="CCAT" width="200"></a>
  <br>
  Cisco Config Analysis Tool 
  <br>
</h1>

[![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-green.svg)](https://opensource.org/licenses/GPL-3.0)
[![Black Hat Arsenal EU 2018](https://img.shields.io/badge/Black%20Hat%20Arsenal-EU%202018-white.svg)](https://blackhat.com/eu-18/arsenal/schedule/#ccat-cisco-config-analysis-tool-12603)

This tool is designed to analyze the configuration files of Cisco devices. 

The [list of checks](https://github.com/cisco-config-analysis-tool/ccat/wiki/List-of-the-checks) is based on the [Cisco Guide to Harden Cisco IOS Devices](https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html).

## Installation
`pip3 install -r requirements.txt` 

## Usage  
The simplest way to use:
`python3 ccat.py configuration_file`

Windows:
```cmd
ccat.exe configuration_file
```

### Commands
- `<config_directory>` - path to the configuration file or directory with configuration files
- `-vlanmap <path_to_file>` - path to [vlanmap file](https://github.com/cisco-config-analysis-tool/ccat/wiki/Vlanmap-file)
- `-output <result_html_files_directory>` - path to output HTML files directory
- `--storm_level` - the appropriate level for storm-control (by default value = 80)
- `--max_number_mac` - maximum number of mac-addresses for port-security (by default value = 10)
- `--disabled-interfaces` - check interfaces even if they are turned off
- `--no-console-display` - output analysis results in HTML files directory or into network graph
- `--dump-creds` - dump usernames, passwords and hashes from configs
- `--graph` - builds a network map of VLANs (you may leave the argument empty to get into interactive mode or define a file name for graph output in png extension)


Extended options example:
```bash
python3 ccat.py ./configs -output ./out -vlanmap vlmap.txt \
  --storm_level 40.0 \
  --max_number_mac 100 \
  --disabled-interfaces \
  --no-console-display \
  --graph network_map
```

