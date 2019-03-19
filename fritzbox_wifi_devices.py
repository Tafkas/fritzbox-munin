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
  env.fritzbox_password [fritzbox password]
  env.fritzbox_username [optional: fritzbox username]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import re
import sys

import fritzbox_helper as fh

locale = os.environ.get('locale', 'de')
patternLoc = {"de": "(\d+) WLAN", "en": "(\d+) wireless LAN"}

PAGE = '/system/energy.lua'
pattern = re.compile(patternLoc[locale])


def get_connected_wifi_devices():
    """gets the numbrer of currently connected wifi devices"""

    server = os.environ['fritzbox_ip']
    password = os.environ['fritzbox_password']

    if "fritzbox_username" in os.environ:
        fritzuser = os.environ['fritzbox_username']
        session_id = fh.get_session_id(server, password, fritzuser)
    else:
        session_id = fh.get_session_id(server, password)
    data = fh.get_page_content(server, session_id, PAGE)
    m = re.search(pattern, data)
    if m:
        connected_devices = int(m.group(1))
        print('wifi.value %d' % connected_devices)


def print_config():
    print('graph_title AVM Fritz!Box Connected Wifi Devices')
    print('graph_vlabel Number of devices')
    print('graph_args --base 1000')
    print('graph_category network')
    print('graph_order wifi')
    print('wifi.label Wifi Connections on 2.4 & 5 Ghz')
    print('wifi.type GAUGE')
    print('wifi.graph LINE1')
    print('wifi.info Wifi Connections on 2.4 & 5 Ghz')
    if os.environ.get('host_name'):
        print("host_name " + os.environ['host_name'])


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print('yes')
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_connected_wifi_devices()
        except:
            sys.exit("Couldn't retrieve connected fritzbox wifi devices")
