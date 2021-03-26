#!/usr/bin/env python
"""
  fritzbox_traffic - A munin plugin for Linux to monitor AVM Fritzbox WAN traffic
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
        sys.exit("Couldn't get WAN traffic")

    traffic = fs.transmission_rate
    down_traffic = traffic[1]
    print("down.value %d" % down_traffic)

    up_traffic = traffic[0]
    print("up.value %d" % up_traffic)

    if not os.environ.get("traffic_remove_max"):
        max_traffic = fs.max_bit_rate
        max_down_traffic = max_traffic[1]
        print("maxdown.value %d" % max_down_traffic)

        max_up_traffic = max_traffic[0]
        print("maxup.value %d" % max_up_traffic)


def print_config():
    print("graph_title AVM Fritz!Box WAN traffic")
    print("graph_args --base 1000")
    print("graph_vlabel bits in (-) / out (+) per \${graph_period}")
    print("graph_category network")
    print("graph_order down up maxdown maxup")
    print("down.label received")
    print("down.type DERIVE")
    print("down.graph no")
    print("down.cdef down,8,*")
    print("down.min 0")
    print("down.max 1000000000")
    print("up.label bps")
    print("up.type DERIVE")
    print("up.draw AREA")
    print("up.cdef up,8,*")
    print("up.min 0")
    print("up.max 1000000000")
    print("up.negative down")
    print("up.info Traffic of the WAN interface.")
    if not os.environ.get("traffic_remove_max"):
        print("maxdown.label received")
        print("maxdown.type GAUGE")
        print("maxdown.graph no")
        print("maxup.label MAX")
        print("maxup.type GAUGE")
        print("maxup.negative maxdown")
        print("maxup.draw LINE1")
        print("maxup.info Maximum speed of the WAN interface.")
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
            sys.exit("Couldn't retrieve fritzbox traffic")
