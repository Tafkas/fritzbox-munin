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

import requests
from lxml import etree


def get_base_uri(host, port=0, tls=False):
    DEFAULT_PORTS = (80, 443)
    SCHEMES = ('http', 'https')
    if port and port != DEFAULT_PORTS[tls]:
        return '{}://{}:{}'.format(SCHEMES[tls], host, port)
    else:
        return '{}://{}'.format(SCHEMES[tls], host)


def get_session_id(server, password, port=0, tls=False, username=None):
    """Obtains the session id after login into the Fritzbox.
    See https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_Technical_Note_-_Session_ID.pdf
    for deteils (in German).

    :param server: the ip address of the Fritzbox
    :param password: the password to log into the Fritzbox webinterface
    :param port: the port the Fritzbox webserver runs on
    :return: the session id
    """

    base_uri = get_base_uri(server, port, tls)
    headers = {"Accept": "application/xml",
               "Content-Type": "text/plain"}

    url = '{}/login_sid.lua'.format(base_uri)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.SSLError) as err:
        print(err)
        sys.exit(1)

    params = {}
    root = etree.fromstring(r.content)
    session_id = root.xpath('//SessionInfo/SID/text()')[0]
    if session_id == "0000000000000000":
        challenge = root.xpath('//SessionInfo/Challenge/text()')[0]
        challenge_bf = ('{}-{}'.format(challenge, password)).encode('utf-16le')
        m = hashlib.md5()
        m.update(challenge_bf)
        response_bf = '{}-{}'.format(challenge, m.hexdigest().lower())
        params['response'] = response_bf
    else:
        return session_id

    if username is not None:
        params['username'] = username

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml",
               "Content-Type": "application/x-www-form-urlencoded"}

    url = '{}/login_sid.lua'.format(base_uri)
    try:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.SSLError) as err:
        print(err)
        sys.exit(1)

    root = etree.fromstring(r.content)
    session_id = root.xpath('//SessionInfo/SID/text()')[0]
    if session_id == "0000000000000000":
        print("ERROR - No SID received because of invalid password")
        sys.exit(0)
    return session_id


def get_page_content(server, session_id, page, port=0, tls=False):
    """Fetches a page from the Fritzbox and returns its content

    :param server: the ip address of the Fritzbox
    :param session_id: a valid session id
    :param page: the page you are regquesting
    :param port: the port the Fritzbox webserver runs on
    :return: the content of the page
    """

    base_uri = get_base_uri(server, port, tls)
    headers = {"Accept": "application/xml",
               "Content-Type": "text/plain"}
    params = {"sid": session_id}

    url = '{}/{}'.format(base_uri, page)
    try:
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
    except (requests.exceptions.HTTPError,
            requests.exceptions.SSLError) as err:
        print(err)
        sys.exit(1)
    return r.content


def get_xhr_content(server, session_id, page, port=0, tls=False):
    """Fetches the xhr content from the Fritzbox and returns its content

    :param server: the ip address of the Fritzbox
    :param session_id: a valid session id
    :param page: the page you are regquesting
    :param port: the port the Fritzbox webserver runs on
    :return: the content of the page
    """

    base_uri = get_base_uri(server, port, tls)
    headers = {"Accept": "application/xml",
               "Content-Type": "application/x-www-form-urlencoded"}

    url = '{}/data.lua'.format(base_uri)
    data = {"xhr": 1,
            "sid": session_id,
            "lang": "en",
            "page": page,
            "xhrId": "all",
            "no_sidrenew": ""
            }
    try:
        r = requests.post(url, data=data, headers=headers)
    except (requests.exceptions.HTTPError,
            requests.exceptions.SSLError) as err:
        print(err)
        sys.exit(1)
    return r.content
