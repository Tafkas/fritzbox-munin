#!/usr/bin/env python
"""
  fritzbox_memory_usage - A munin plugin for Linux to monitor AVM Fritzbox
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

PAGE = 'ecoStat'
USAGE = ['strict', 'cache', 'free']
hostname = os.path.basename(__file__).split('_')[1]


def get_memory_usage():
    """get the current memory usage"""

    server = hostname
    password = os.environ['fritzbox_password']

    session_id = fh.get_session_id(server, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)
    for i, usage in enumerate(USAGE):
        print('%s.value %s' % (usage, data['data']['ramusage']['series'][i][-1]))


def print_config():
    print("host_name %s" % hostname)
    print("graph_title AVM Fritz!Box Memory")
    print("graph_vlabel %")
    print("graph_args --base 1000 -r --lower-limit 0 --upper-limit 100")
    print("graph_category system")
    print("graph_order strict cache free")
    print("graph_info This graph shows what the Fritzbox uses memory for.")
    print("graph_scale no")
    print("strict.label strict")
    print("strict.type GAUGE")
    print("strict.draw AREA")
    print("cache.label cache")
    print("cache.type GAUGE")
    print("cache.draw STACK")
    print("free.label free")
    print("free.type GAUGE")
    print("free.draw STACK")
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
            get_memory_usage()
        except:
            sys.exit("Couldn't retrieve fritzbox memory usage")
