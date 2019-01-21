#Author: Chris Gulledge
# This script pings a remote host at a user controlled interval. If the host appears to be down,
# powertoggle.py is called to send a JSON request to a TP-Link HS100 smart plug.
# Assuming the monitored device is drawing power from the HS100 smart plug, the device will be power cycled.
# Additional information on how to get the required parameters token, deviceid can be accessed at:
# http://itnerd.space/2017/01/22/how-to-control-your-tp-link-hs100-smartplug-from-internet/

import subprocess as sp
import time
import argparse
from builtins import print
import powertoggle

def main():
    tp_link_token = ''                 #The HS100 TPLink token
    device_id = ''                     #The HS100 device ID
    ping_delay = 5                     #Delay in seconds between ping attempts.
    remote_host = ''                   #Remote host
    time_between_failed_attempts = 60  #If the HS100 plug does not respond, how long to wait before retry.
    max_allowed_downtime = 60          #If the monitored server does not respond in this time, proceed with
                                       #power cycle. Measured in seconds.
    power_off_time = 10                #How long the device should stay off.
    power_on_delay = 180               #How long should the device have to boot up and get connected to network?

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--token', help='The token associated with your TP-Link smartplug.', required=True)
    parser.add_argument('--deviceid', help='The device ID associated with your TP-Link smartplug.', required=True)
    parser.add_argument('--remhost', help='The remote host to check for connectivity.', required=True,type=str)
    parser.add_argument('--pingdelay', help='Time between pings in seconds. Default 5.', required=False)
    parser.add_argument('--retrytime', help='If power cycle attempt fails, retry after '
                                            'this many seconds. Default 60.',
                        required=False, type=int)

    parser.add_argument('--powerofftime', help='How long to wait between power cycles. '
                                               'Default 10.', required=False, type=int)

    parser.add_argument('--powerondelay', help='Once device is powered on, how long to wait for it to be active. '
                                               'Default 180 seconds.', required=False, type=int)

    args = parser.parse_args()
    if args.token:
        tp_link_token = args.token
    if args.deviceid:
        device_id = args.deviceid
    if args.remhost:
        remote_host = args.remhost
    if args.pingdelay:
        ping_delay = int(args.pingdelay)

    if args.retrytime:
        time_between_failed_attempts = int(args.retrytime)

    if args.powerofftime:
        power_off_time = int(args.powerofftime)
    if args.powerondelay:
        power_on_delay = int(args.powerondelay)

    time_since_last_seen = 0.00
    device_powered_off = False
    try_to_ping_host = True
    time_server_has_been_down = 0

    while True:

        if try_to_ping_host:
            pingrc = pingHost(remote_host)

            if pingrc == 0:
                time_since_last_seen = time.time()
                time.sleep(ping_delay)
            else:
                current_time = time.time()
                time_server_has_been_down = current_time - time_since_last_seen

        if (time_server_has_been_down >= max_allowed_downtime) and device_powered_off is False:
                state = 0
                try_to_ping_host = False
                response = powertoggle.power_toggle(tp_link_token, device_id, state)

                if response == 0:
                    device_powered_off = True
                    time.sleep(power_off_time)
                else:
                    device_powered_off = False
                    time.sleep(time_between_failed_attempts)

        if (time_server_has_been_down >= max_allowed_downtime) and device_powered_off is True:
                state = 1
                response = powertoggle.power_toggle(tp_link_token, device_id, state)

                if response == 0:
                    time.sleep(power_on_delay)
                    device_powered_off = False
                    try_to_ping_host = True
                    time_server_has_been_down = 0
                else:
                    try_to_ping_host = True
                    time.sleep(time_between_failed_attempts)


def pingHost(remote_host):
    param = '-c'
    command = ['ping', param, '1', remote_host]
    child = sp.Popen(command, stdout=None)
    child.communicate()
    rc = child.poll()
    return rc
    

main()
