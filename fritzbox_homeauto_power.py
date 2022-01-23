#!/usr/bin/env python3
"""
  fritzbox_homeauto_power - A munin plugin for Linux to monitor AVM Fritzbox homeautomation power consumption
  Copyright (C) 2022 Alexander Knöbel
  Author: Alexander Knöbel
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  This plugin requires the fritzconnection plugin. To install it using pip:
  pip install fritzconnection
  This plugin supports the following munin configuration parameters:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_username [fritzbox username]
  env.fritzbox_password [fritzbox password]

  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import sys

from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

server = os.environ["fritzbox_ip"]
username = os.environ["fritzbox_username"]
password = os.environ["fritzbox_password"]

def print_values():
    try:
        fha = FritzHomeAutomation(address=server, user=username, password=password)
    except Exception as e:
        sys.exit("Couldn't get home automation")

    info = fha.device_informations()
    for device in info:
        if device["NewMultimeterIsEnabled"] == "ENABLED":
           identifier = device["NewAIN"].replace(" ","_")
           print(identifier + ".value %.2f" % (int(device["NewMultimeterPower"]) / 100))

def print_config():
    try:
        fha = FritzHomeAutomation(address=server, user=username, password=password)
    except Exception as e:
        sys.exit("Couldn't get home automation")

    print("graph_title AVM Fritz!Box Homeautomation Power Consumption")
    print("graph_args -l 0")
    print("graph_vlabel Watt")
    print("graph_scale no")
    print("graph_category sensors")
    info = fha.device_informations()
    for device in info:
        if device["NewMultimeterIsEnabled"] == "ENABLED":
            identifier = device["NewAIN"].replace(" ","_")
            print(identifier + ".label " + device["NewDeviceName"] + " Power")
            print(identifier + ".draw LINE1")
    if os.environ.get("host_name"):
        print("host_name " + os.environ["host_name"])


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "config":
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == "autoconf":
        print("yes")  # Some docs say it'll be called with fetch, some say no arg at all
    elif len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "fetch"):
        try:
            print_values()
        except:
            sys.exit("Couldn't retrieve fritzbox home automation")
