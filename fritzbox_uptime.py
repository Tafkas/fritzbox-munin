#!/usr/bin/env python3
"""
  fritzbox_uptime - A munin plugin for Linux to monitor AVM Fritzbox
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
patternLoc = {"de": r"(\d+)\s(Tag|Stunden|Minuten)",
              "en": r"(\d+)\s(days|hours|minutes)"}
dayLoc = {"de": "Tag", "en": "days"}
hourLoc = {"de": "Stunden", "en": "hours"}
minutesLoc = {"de": "Minuten", "en": "minutes"}

PAGE = 'energy'
pattern = re.compile(patternLoc[locale])


def get_uptime():
    """get the current uptime"""

    server = os.getenv('fritzbox_ip')
    password = os.getenv('FRITZ_PASSWORD')

    if "FRITZ_USERNAME" in os.environ:
        fritzuser = os.getenv('FRITZ_USERNAME')
        session_id = fh.get_session_id(server, password, fritzuser)
    else:
        session_id = fh.get_session_id(server, password)
    xhr_data = fh.get_xhr_content(server, session_id, PAGE)
    data = json.loads(xhr_data)
    for d in data['data']['drain']:
        if 'aktiv' in d['statuses']:
            matches = re.finditer(pattern, d['statuses'])
            if matches:
                hours = 0.0
                for m in matches:
                    if m.group(2) == dayLoc[locale]:
                        hours += 24 * int(m.group(1))
                    if m.group(2) == hourLoc[locale]:
                        hours += int(m.group(1))
                    if m.group(2) == minutesLoc[locale]:
                        hours += int(m.group(1)) / 60.0
                uptime = hours / 24
                print("uptime.value %.2f" % uptime)


def print_config():
    print("graph_title AVM Fritz!Box Uptime")
    print("graph_args --base 1000 -l 0")
    print('graph_vlabel uptime in days')
    print("graph_scale no'")
    print("graph_category system")
    print("uptime.label uptime")
    print("uptime.draw AREA")
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
            get_uptime()
        except Exception as e:
            sys.exit(f"Couldn't retrieve fritzbox uptime; {e}")
