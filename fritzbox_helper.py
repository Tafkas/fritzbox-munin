#!/usr/bin/env python
"""
  fritzbox_helper - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
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

  The initial script was inspired by
  https://www.linux-tips-and-tricks.de/en/programming/389-read-data-from-a-fritzbox-7390-with-python-and-bash
  framp at linux-tips-and-tricks dot de
"""

import hashlib
import sys
import os

import requests
from lxml import etree

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0"


def get_session_id():
    """Obtains the session id after login into the Fritzbox.
    See https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_Technical_Note_-_Session_ID.pdf
    for deteils (in German).

    :return: the session id
    """

    server = os.environ['fritzbox_ip']
    if 'fritzbox_port' in os.environ :
        port = os.environ['fritzbox_port']
    else :
        port = 80
    if 'fritzbox_user' in os.environ :
        user = os.environ['fritzbox_user']
    else :
        user = ""
    password = os.environ['fritzbox_password']

    headers = {"Accept": "application/xml",
               "Content-Type": "text/plain",
               "User-Agent": USER_AGENT}

    url = 'http://{}:{}/login_sid.lua'.format(server, port)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)

    root = etree.fromstring(r.content)
    session_id = root.xpath('//SessionInfo/SID/text()')[0]
    if session_id == "0000000000000000":
        challenge = root.xpath('//SessionInfo/Challenge/text()')[0]
#        challenge_bf = ('{}-{}'.format(challenge, password)).decode('iso-8859-1').encode('utf-16le')
        challenge_bf = ('{}-{}'.format(challenge, password)).encode('utf-16le')
        m = hashlib.md5()
        m.update(challenge_bf)
        response_bf = '{}-{}'.format(challenge, m.hexdigest().lower())
    else:
        return session_id

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml",
               "Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": USER_AGENT}

    if user :
        url = 'http://{}:{}/login_sid.lua?username={}&response={}'.format(server, port, user, response_bf)
    else :
        url = 'http://{}:{}/login_sid.lua?response={}'.format(server, port, response_bf)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)

    root = etree.fromstring(r.content)
    session_id = root.xpath('//SessionInfo/SID/text()')[0]
    if session_id == "0000000000000000":
        print("ERROR - No SID received because of invalid password")
        sys.exit(0)
    return session_id


def get_page_content(session_id, page):
    """Fetches a page from the Fritzbox and returns its content

    :param session_id: a valid session id
    :param page: the page you are regquesting
    :param port: the port the Fritzbox webserver runs on
    :return: the content of the page
    """

    server = os.environ['fritzbox_ip']
    if 'fritzbox_port' in os.environ :
        port = os.environ['fritzbox_port']
    else :
        port = 80
    headers = {"Accept": "application/xml",
               "Content-Type": "text/plain",
               "User-Agent": USER_AGENT}
    if "?" in page :
        url = 'http://{}:{}/{}&sid={}'.format(server, port, page, session_id)
    else :
        url = 'http://{}:{}/{}?sid={}'.format(server, port, page, session_id)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    return r.content


def get_xhr_content(session_id, page):
    """Fetches the xhr content from the Fritzbox and returns its content
    :param server: the ip address of the Fritzbox
    :param session_id: a valid session id
    :param page: the page you are requesting
    :param port: the port the Fritzbox webserver runs on
    :return: the content of the page
    """
    server = os.environ['fritzbox_ip']
    if 'fritzbox_port' in os.environ :
        port = os.environ['fritzbox_port']
    else :
        port = 80

    headers = {"Accept": "application/xml",
               "Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": USER_AGENT}

    url = 'http://{}:{}/data.lua'.format(server, port)
    data = {"xhr": 1,
            "sid": session_id,
            "lang": "en",
            "page": page,
            "xhrId": "all",
            "no_sidrenew": ""
           }
    try:
        r = requests.post(url, data=data, headers=headers)
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    return r.content
