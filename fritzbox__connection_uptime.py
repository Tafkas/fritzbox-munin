#!/usr/bin/env python
"""
  fritzbox_connection_uptime - A munin plugin for Linux to monitor AVM Fritzbox connection uptime
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt

  Updated to fritzconnection library version 1.3.1
  Copyright (C) 2020 Oliver Edelamnn
  Author: Oliver Edelmann

  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  This plugin requires the fritzconnection plugin. To install it using pip:
  pip install fritzconnection
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import sys

from fritzconnection.lib.fritzstatus import FritzStatus

hostname = os.path.basename(__file__).split('_')[1]

def print_values():
    try:
        conn = FritzStatus(address=hostname, password=os.environ['fritzbox_password'])
    except Exception:
        sys.exit("Couldn't get connection uptime")

    uptime = conn.uptime
    print('uptime.value %.2f' % (int(uptime) / 3600.0))


def print_config():
    print("host_name %s" % hostname)
    print("graph_title AVM Fritz!Box Connection Uptime")
    print("graph_args --base 1000 -l 0")
    print('graph_vlabel uptime in hours')
    print("graph_scale no'")
    print("graph_category network")
    print("uptime.label uptime")
    print("uptime.draw AREA")
    if os.environ.get('host_name'):
        print("host_name " + os.environ['host_name'])


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print("yes")  # Some docs say it'll be called with fetch, some say no arg at all
    elif len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == 'fetch'):
        try:
            print_values()
        except:
            sys.exit("Couldn't retrieve fritzbox connection uptime")
