#!/usr/bin/env python3
"""
  fritzbox_cpu_temperature - A munin plugin for Linux to monitor AVM Fritzbox
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
import sys
import fritzbox_helper as fh

PAGE = 'ecoStat'


def get_cpu_temperature():
    """get the current cpu temperature"""

    server = os.getenv('fritzbox_ip')
    password = os.getenv('FRITZ_PASSWORD')

    if "FRITZ_USERNAME" in os.environ:
        fritzuser = os.getenv('FRITZ_USERNAME')
        session_id = fh.get_session_id(server, password, fritzuser)
    else:
        session_id = fh.get_session_id(server, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)
    print('temp.value %d' % (int(data['data']['cputemp']['series'][0][-1])))


def print_config():
    if os.environ.get('host_name'):
        print("host_name " + os.getenv('host_name'))
        print("graph_title Temperatures")
    else:
        print("graph_title AVM Fritz!Box CPU temperature")
    print("graph_vlabel degrees Celsius")
    print("graph_category sensors")
    print("graph_order tmp")
    print("graph_scale no")
    print("temp.label CPU temperature")
    print("temp.type GAUGE")
    print("temp.graph LINE1")
    print("temp.min 0")
    print("temp.info Fritzbox CPU temperature")


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print('yes')
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        get_cpu_temperature()
