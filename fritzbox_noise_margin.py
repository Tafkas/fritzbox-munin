#!/usr/bin/env python3
"""
  fritzbox_attenuation - A munin plugin for Linux to monitor AVM Fritzbox noise margin
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
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

from fritzconnection.lib.fritzstatus import FritzStatus

server = os.environ["fritzbox_ip"]
username = os.environ["fritzbox_username"]
password = os.environ["fritzbox_password"]


def print_values():
    try:
        fs = FritzStatus(address=server, user=username, password=password)
    except Exception as e:
        sys.exit("Couldn't get noise margin")

    noise_margin = fs.noise_margin
    print("up.value %.2f" % (int(noise_margin[0]) / 10.0))
    print("down.value %.2f" % (int(noise_margin[1]) / 10.0))


def print_config():
    print("graph_title AVM Fritz!Box Noise Margin")
    print("graph_vlabel noise margin in dB")
    print("graph_scale no")
    print("graph_category network")
    print("down.type GAUGE")
    print("down.label downstram")
    print("down.draw AREA")
    print("up.type GAUGE")
    print("up.label upstream")
    print("up.draw AREA")
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
            sys.exit("Couldn't retrieve fritzbox noise_margin")
