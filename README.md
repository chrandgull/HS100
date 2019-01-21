# HS100
This repository provides python3 scripts to work with the HS100 smartplug. 

Scripts:
healthcheck.py - Pings a given IP address at a user interval. 
If the remote host does not respond to ping for a given period of time then powercycle.py is 
called to power cycle the HS100 smart plug. If the remote host doesn't support or respond to ping requests, don't use this. 

powercycle.py - Responsible for sending a command to the TP-Link servers. Requires a token and device ID to work. 

Dependancies:

Python3 - Tested with version 3.5.3

Requests Library: Tested with version 2.12.4

Purpose:

This script can be used to power cycle a server or appliance that is not responding that normally responds to ping requests within an given amount of time. 

More information about interfacing with the HS100 smartplug can be found here:

http://itnerd.space/2017/01/22/how-to-control-your-tp-link-hs100-smartplug-from-internet/

