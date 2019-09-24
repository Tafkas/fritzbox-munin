#!/usr/bin/env python3
"""
  fritzbox_wifi_devices - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.FRITZ_PASSWORD [fritzbox password]
  env.FRITZ_USERNAME [optional: fritzbox username]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""
import json
import os
import re
import sys

import fritzbox_helper as fh

locale = os.environ.get('locale', 'de')
patternLoc = {"de": r"(\d+) WLAN",
              "en": r"(\d+) wireless LAN"}

PAGE = 'energy'
pattern = re.compile(patternLoc[locale])


def get_connected_wifi_devices():
    """gets the numbrer of currently connected wifi devices"""

    server = os.getenv('fritzbox_ip')
    password = os.getenv('FRITZ_PASSWORD')

    if "FRITZ_USERNAME" in os.environ:
        fritzuser = os.getenv('FRITZ_USERNAME')
        session_id = fh.get_session_id(server, password, fritzuser)
    else:
        session_id = fh.get_session_id(server, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)
    m = re.search(pattern, data['data']['drain'][2]['statuses'][-1])
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
        print("host_name " + os.getenv('host_name'))


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print('yes')
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_connected_wifi_devices()
        except Exception as e:
            sys.exit(f"Couldn't retrieve connected fritzbox wifi devices: {e}")
