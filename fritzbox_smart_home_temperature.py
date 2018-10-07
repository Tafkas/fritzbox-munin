#!/usr/bin/env python
"""
  fritzbox_smart_home_temperature - A munin plugin for Linux to monitor AVM Fritzbox SmartHome temperatures
  Copyright (C) 2018 Bernd Oerding
  Author: Bernd Oerding
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_port [optional port, default: 80]
  env.fritzbox_user [optionial, if you configured the FritzBox to use user and password]
  env.fritzbox_password [fritzbox password]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import os
import re
import sys
import fritzbox_helper as fh
from lxml import etree
from unidecode import unidecode

PAGE = 'webservices/homeautoswitch.lua?switchcmd=getdevicelistinfos'


def get_smart_home_temperature(debug=False):
    """get the current cpu temperature"""

    session_id = fh.get_session_id()
    data = fh.get_page_content(session_id, PAGE)
    root = etree.fromstring(data)
    if debug :
        print(etree.tostring(root, pretty_print=True))
    for d in root :
        id = d.xpath("@id")[0]
        present = int(d.xpath("present/text()")[0])
        if present :
            temp= float(d.xpath("temperature/celsius/text()")[0])/10
            print ("t{}.value {}".format(id,temp))


def print_config():
    print("graph_title AVM Fritz!Box SmartHome temperature")
    print("graph_vlabel degrees Celsius")
    print("graph_category sensors")
    print("graph_scale no")
    server = os.environ['fritzbox_ip']
    user = os.environ['fritzbox_user']
    password = os.environ['fritzbox_password']

    session_id = fh.get_session_id()
    data = fh.get_page_content(session_id, PAGE)
    root = etree.fromstring(data)
    for d in root :
        id = d.xpath("@id")[0]
        identifier = d.xpath("@identifier")[0]
        name = d.xpath("name/text()")[0]
        name = unidecode(unicode(name))
        pname = d.xpath("@productname")[0]
        
        print ("t{}.label {}".format(id,name)) 
        print ("t{}.type GAUGE".format(id)) 
        print ("t{}.graph LINE".format(id)) 
        print ("t{}.info Temperature [{} - {}]".format(id,pname,identifier)) 
    if os.environ.get('host_name'):
        print("host_name " + os.environ['host_name'])


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        print_config()
    elif len(sys.argv) == 2 and sys.argv[1] == 'autoconf':
        print('yes')
    elif len(sys.argv) == 2 and sys.argv[1] == 'debug':
        get_smart_home_temperature(True)
    elif len(sys.argv) == 1 or len(sys.argv) == 2 and sys.argv[1] == 'fetch':
        # Some docs say it'll be called with fetch, some say no arg at all
       try:
            get_smart_home_temperature()
       except:
            sys.exit("Couldn't retrieve fritzbox smarthome temperatures")
