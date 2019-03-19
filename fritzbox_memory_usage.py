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
  env.fritzbox_username [optional: fritzbox username]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import re
import sys
import fritzbox_helper as fh

PAGE = '/system/ecostat.lua'
pattern = re.compile('Query[1-3]\s="(\d{1,3})')
USAGE = ['free', 'cache', 'strict']


def get_memory_usage():
    """get the current memory usage"""

    server = os.environ['fritzbox_ip']
    password = os.environ['fritzbox_password']

    if "fritzbox_username" in os.environ:
        fritzuser = os.environ['fritzbox_username']
        session_id = fh.get_session_id(server, password, fritzuser)
    else:
        session_id = fh.get_session_id(server, password)
    data = fh.get_page_content(server, session_id, PAGE)
    matches = re.finditer(pattern, data)
    if matches:
        data = zip(USAGE, [m.group(1) for m in matches])
        for d in data:
            print('%s.value %s' % (d[0], d[1]))


def print_config():
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
