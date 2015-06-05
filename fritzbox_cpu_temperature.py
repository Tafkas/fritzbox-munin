#!/usr/bin/env python
"""
  fritzbox_cpu_temperature - A munin plugin for Linux to monitor AVM Fritzbox
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

import os
import re
import sys
import fritzbox_helper as fh

PAGE = '/system/ecostat.lua'
pattern = re.compile(".*/(StatTemperature)\".*=.*\"(.*?)\"")


def get_cpu_temperature():
    """get the current cpu temperature"""

    server = os.environ['fritzbox_ip']
    password = os.environ['fritzbox_password']

    sid = fh.get_sid(server, password)
    data = fh.get_page(server, sid, PAGE)

    m = re.search(pattern, data)
    if m:
        print 'temp.value %d' % (int(m.group(2).split(',')[0]))


def print_config():
    print "graph_title AVM Fritz!Box CPU temperature"
    print "graph_vlabel degrees Celsius"
    print "graph_category sensors"
    print "graph_order tmp"
    print "graph_scale no"
    print "temp.label CPU temperature"
    print "temp.type GAUGE"
    print "temp.graph LINE1"
    print "temp.min 0"
    print "temp.info Fritzbox CPU temperature"


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print 'yes'
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
        try:
            get_cpu_temperature()
        except:
            sys.exit("Couldn't retrieve fritzbox cpu temperature")
