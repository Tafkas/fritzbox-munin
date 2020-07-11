#!/usr/bin/env python
"""
  fritzbox_cpu_usage - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_password [fritzbox password]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""
import json
import os
import sys
import fritzbox_helper as fh

PAGE = { '7': 'ecoStat', '6': 'system/ecostat.lua' }


def get_cpu_usage():
    """get the current cpu usage"""

    server = os.environ['fritzbox_ip']
    password = os.environ['fritzbox_password']

    session_id = fh.get_session_id(server, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)
    print('cpu.value %d' % (int(data['data']['cpuutil']['series'][0][-1])))


def print_config():
    hostname = os.path.basename(__file__).split('_')[1]
    print("host_name %s" % hostname)
    print("graph_title AVM Fritz!Box CPU usage")
    print("graph_vlabel %")
    print("graph_category system")
    print("graph_order cpu")
    print("graph_scale no")
    print("cpu.label system")
    print("cpu.type GAUGE")
    print("cpu.graph AREA")
    print("cpu.min 0")
    print("cpu.info Fritzbox CPU usage")
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
            get_cpu_usage()
        except:
            sys.exit("Couldn't retrieve fritzbox cpu usage")
