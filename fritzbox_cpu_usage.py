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
  env.fritzbox_username[fritzbox username]
  env.fritzbox_password [fritzbox password]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import re
import sys
import fritzbox_helper as fh

PAGE = '/system/ecostat.lua'
pattern = re.compile('Query1\s=\s"(\d{1,3})')

# bet box name from first part before '_' in (symlink) file name
boxname = os.path.basename(__file__).rsplit('_')[0]


def get_cpu_usage():
    """get the current cpu usage"""

    server = os.environ['fritzbox_ip']
    username = os.environ['fritzbox_username']
    password = os.environ['fritzbox_password']

    sid = fh.get_sid(server, username, password)
    data = fh.get_page(server, sid, PAGE)

    m = re.search(pattern, data)
    if m:
        print 'cpu.value %d' % (int(m.group(1)))


def print_config():
    print "host_name %s" % boxname
    print "graph_title AVM Fritz!Box CPU usage"
    print "graph_vlabel %"
    print "graph_category system"
    print "graph_order cpu"
    print "graph_scale no"
    print "cpu.label system"
    print "cpu.type GAUGE"
    print "cpu.graph AREA"
    print "cpu.min 0"
    print "cpu.info Fritzbox CPU usage"


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print 'yes'
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_cpu_usage()
        except:
            sys.exit("Couldn't retrieve fritzbox cpu usage")
