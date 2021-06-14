"""
  fritzbox_helper - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0

  Copyright (c) 2021 Oliver Edelmann
  Author: Oliver Edelmann
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
import os

import requests
import urllib.parse
from lxml import etree

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0"

"""
  Code from https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_Technical_Note_-_Session_ID_deutsch_2021-05-03.pdf
  start
"""
def calculate_pbkdf2_response(challenge: str, password: str) -> str: 
    """ Calculate the response for a given challenge via PBKDF2 """ 
    challenge_parts = challenge.split("$") 
    # Extract all necessary values encoded into the challenge 
    iter1 = int(challenge_parts[1]) 
    salt1 = bytes.fromhex(challenge_parts[2]) 
    iter2 = int(challenge_parts[3]) 
    salt2 = bytes.fromhex(challenge_parts[4]) 
    # Hash twice, once with static salt... 
    hash1 = hashlib.pbkdf2_hmac("sha256", password.encode(), salt1, iter1) 
    # Once with dynamic salt. 
    hash2 = hashlib.pbkdf2_hmac("sha256", hash1, salt2, iter2) 
    return f"{challenge_parts[4]}${hash2.hex()}" 
 
 
def calculate_md5_response(challenge: str, password: str) -> str: 
    """ Calculate the response for a challenge using legacy MD5 """ 
    response = challenge + "-" + password 
    # the legacy response needs utf_16_le encoding 
    response = response.encode("utf_16_le") 
    md5_sum = hashlib.md5() 
    md5_sum.update(response) 
    response = challenge + "-" + md5_sum.hexdigest() 
    return response         
"""
  Code from https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_Technical_Note_-_Session_ID_deutsch_2021-05-03.pdf
  start
"""

def get_session_id(server, password, port=80):
    """Obtains the session id after login into the Fritzbox.
    See https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM_Technical_Note_-_Session_ID.pdf
    for deteils (in German).

    :param server: the ip address of the Fritzbox
    :param password: the password to log into the Fritzbox webinterface
    :param port: the port the Fritzbox webserver runs on
    :return: the session id
    """

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
    challenge = root.xpath('//SessionInfo/Challenge/text()')[0]
    new_login = True

    try:
        user_id = root.xpath('//SessionInfo/Users/User/text()')[0]
    except IndexError:
        new_login = False
    
    if "fritzbox_user" in os.environ:
        user_id = os.environ['fritzbox_user'] 

    if session_id == "0000000000000000":
        if challenge.startswith("2$"):
            response_bf = calculate_pbkdf2_response(challenge, password)
        else:
            response_bf = calculate_md5_response(challenge, password)
    else:
        return session_id

    headers = {"Accept": "text/html,application/xhtml+xml,application/xml",
               "Content-Type": "application/x-www-form-urlencoded",
               "User-Agent": USER_AGENT}

    try:
        if new_login:
            url = 'http://{}:{}/login_sid.lua?version=2'.format(server, port)
            data = {"username": user_id,"response": response_bf}
            r = requests.post(url, urllib.parse.urlencode(data).encode(), headers=headers)
        else:
            url = 'http://{}:{}/login_sid.lua?&response={}'.format(server, port, response_bf) 
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


def get_page_content(server, session_id, page, port=80):
    """Fetches a page from the Fritzbox and returns its content

    :param server: the ip address of the Fritzbox
    :param session_id: a valid session id
    :param page: the page you are regquesting
    :param port: the port the Fritzbox webserver runs on
    :return: the content of the page
    """

    headers = {"Accept": "application/xml",
               "Content-Type": "text/plain",
               "User-Agent": USER_AGENT}

    url = 'http://{}:{}/{}?sid={}'.format(server, port, page, session_id)
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    return r.content


def get_xhr_content(server, session_id, page, port=80):
    """Fetches the xhr content from the Fritzbox and returns its content

    :param server: the ip address of the Fritzbox
    :param session_id: a valid session id
    :param page: the page you are regquesting
    :param port: the port the Fritzbox webserver runs on
    :return: the content of the page
    """

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
