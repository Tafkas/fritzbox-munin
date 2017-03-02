#!/usr/bin/env python
"""
  fritzbox_wifi_devices - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_username [fritzbox username]
  env.fritzbox_password [fritzbox password]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import re
import sys
import fritzbox_helper as fh

PAGE = '/system/energy.lua'
pattern = re.compile("(\d+) WLAN")

# bet box name from first part before '_' in (symlink) file name
boxname = os.path.basename(__file__).rsplit('_')[0]


def get_connected_wifi_devices():
    """gets the numbrer of currently connected wifi devices"""

    server = os.environ['fritzbox_ip']
    username = os.getenv('fritzbox_username', "None")
    password = os.environ['fritzbox_password']

    sid = fh.get_sid(server, username, password)
    data = fh.get_page(server, sid, PAGE)
    m = re.search(pattern, data)
    if m:
        connected_devices = int(m.group(1))
        print 'wifi.value %d' % connected_devices


def print_config():
    print "host_name %s" % boxname
    print 'graph_title AVM Fritz!Box Connected Wifi Devices'
    print 'graph_vlabel Number of devices'
    print 'graph_args --base 1000'
    print 'graph_category network'
    print 'graph_order wifi'
    print 'wifi.label Wifi Connections on 2.4 & 5 Ghz'
    print 'wifi.type GAUGE'
    print 'wifi.graph LINE1'
    print 'wifi.info Wifi Connections on 2.4 & 5 Ghz'


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print 'yes'
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_connected_wifi_devices()
        except:
            sys.exit("Couldn't retrieve connected fritzbox wifi devices")
