#!/usr/bin/env python
"""
  fritzbox_helper - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  If you've put your gunicorn pid somewhere other than the
  default /var/run/gunicorn.pid, you can add a section like
  this to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.password [fritzbox password]
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf
"""

import hashlib
import httplib
import os
import re
import sys
from xml.dom import minidom
from io import StringIO, BytesIO

USER_AGENT = "Mozilla/5.0 (U; Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0"

def get_sid(server,password,port=80):
    """Obtains the sid after login into the fritzbox"""
    conn = httplib.HTTPConnection(server+':'+str(port))

    headers = { "Accept" : "application/xml",
                "Content-Type" : "text/plain",
                "User-Agent" : USER_AGENT}

    initialPage='/login_sid.lua'
    conn.request("GET", initialPage, '', headers)
    response = conn.getresponse()
    data = response.read()
    if response.status != 200:
        print "%s %s" % (response.status, response.reason)
        sys.exit(0)
    else:
        theXml = minidom.parseString(data)
        sidInfo = theXml.getElementsByTagName('SID')
        sid=sidInfo[0].firstChild.data
        if sid == "0000000000000000":
            challengeInfo = theXml.getElementsByTagName('Challenge')
            challenge=challengeInfo[0].firstChild.data
            challenge_bf = (challenge + '-' + password).decode('iso-8859-1').encode('utf-16le')
            m = hashlib.md5()
            m.update(challenge_bf)
            response_bf = challenge + '-' + m.hexdigest().lower()
        else:
            return sid

    headers = { "Accept" : "text/html,application/xhtml+xml,application/xml",
                "Content-Type" : "application/x-www-form-urlencoded",
                "User-Agent" : USER_AGENT}

    loginPage="/login_sid.lua?&response=" + response_bf
    conn.request("GET", loginPage, '', headers)
    response = conn.getresponse()
    data = response.read()
    if response.status != 200:
        print "%s %s" % (response.status, response.reason)
        sys.exit(0)
    else:
        sid = re.search('<SID>(.*?)</SID>', data).group(1)
        if sid == "0000000000000000":
            print "ERROR - No SID received because of invalid password"
            sys.exit(0)
        return sid

def get_page(server, sid, page, port=80):
    """Fetches a page from the Fritzbox and returns its content"""
    conn = httplib.HTTPConnection(server+':'+str(port))

    headers = { "Accept" : "application/xml",
                "Content-Type" : "text/plain",
                "User-Agent" : USER_AGENT}

    pageWithSid=page+"?sid="+sid
    conn.request("GET", pageWithSid, '', headers)
    response = conn.getresponse()
    data = response.read()
    if response.status != 200:
        print "%s %s" % (response.status, response.reason)
        print data
        sys.exit(0)
    else:
        return data