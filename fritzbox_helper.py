#!/usr/bin/env python3
"""
  fritzbox_helper - A munin plugin for Linux to monitor AVM Fritzbox
  Copyright (C) 2015 Christian Stade-Schuldt
  Author: Christian Stade-Schuldt
  Like Munin, this plugin is licensed under the GNU GPL v2 license
  http://www.opensource.org/licenses/GPL-2.0
  Add the following section to your munin-node's plugin configuration:

  [fritzbox_*]
  env.fritzbox_ip [ip address of the fritzbox]
  env.fritzbox_username [fritzbox username]
  env.fritzbox_password [fritzbox password]
  
  This plugin supports the following munin configuration parameters:
  #%# family=auto contrib
  #%# capabilities=autoconf

  The initial script was inspired by
  https://www.linux-tips-and-tricks.de/en/programming/389-read-data-from-a-fritzbox-7390-with-python-and-bash
  framp at linux-tips-and-tricks dot de

  New authentication supporting username and password, as well as PBKDF2 support, has been inspired by
  https://avm.de/fileadmin/user_upload/Global/Service/Schnittstellen/AVM%20Technical%20Note%20-%20Session%20ID_englisch.pdf
"""

import hashlib
import sys
import time

import requests
from lxml import etree

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:10.0) Gecko/20100101 Firefox/10.0"

LOGIN_SID_ROUTE = "/login_sid.lua?version=2"


class LoginState:
    def __init__(self, challenge, blocktime):
        self.challenge = challenge
        self.blocktime = blocktime
        self.is_pbkdf2 = challenge.startswith("2$")


def get_session_id(server, username, password, port=80):
    """ Get a sid by solving the PBKDF2 (or MD5) challenge-response process. """
    box_url = "http://{}:{}".format(server, port)
    try:
        state = get_login_state(box_url)
    except Exception as ex:
        raise Exception("failed to get challenge")
    if state.is_pbkdf2:
        # print("PBKDF2 supported")
        challenge_response = calculate_pbkdf2_response(state.challenge, password)
    else:
        # print("Falling back to MD5")
        challenge_response = calculate_md5_response(state.challenge, password)
    if state.blocktime > 0:
        # print(f"Waiting for {state.blocktime} seconds...")
        time.sleep(state.blocktime)
    try:
        sid = send_response(box_url, username, challenge_response)
    except Exception as ex:
        raise Exception("failed to login") from ex
    if sid == "0000000000000000":
        raise Exception("wrong username or password")
    return sid


def get_login_state(box_url):
    """ Get login state from FRITZ!Box using login_sid.lua?version=2 """
    url = box_url + LOGIN_SID_ROUTE
    r = requests.get(url)
    xml = etree.fromstring(r.content)
    challenge = xml.find("Challenge").text
    blocktime = int(xml.find("BlockTime").text)
    return LoginState(challenge, blocktime)


def calculate_pbkdf2_response(challenge, password):
    """ Calculate the response for a given challenge via PBKDF2 """
    challenge_parts = challenge.split("$")
    # Extract all necessary values encoded into the challenge
    iter1 = int(challenge_parts[1])
    salt1 = bytes.fromhex(challenge_parts[2])
    iter2 = int(challenge_parts[3])
    salt2 = bytes.fromhex(challenge_parts[4])
    # Hash twice, once with static salt...
    # Once with dynamic salt.
    hash1 = hashlib.pbkdf2_hmac("sha256", password.encode(), salt1, iter1)
    hash2 = hashlib.pbkdf2_hmac("sha256", hash1, salt2, iter2)
    return f"{challenge_parts[4]}${hash2.hex()}"


def calculate_md5_response(challenge, password):
    """ Calculate the response for a challenge using legacy MD5 """
    response = challenge + "-" + password
    # the legacy response needs utf_16_le encoding
    response = response.encode("utf_16_le")
    md5_sum = hashlib.md5()
    md5_sum.update(response)
    response = challenge + "-" + md5_sum.hexdigest()
    return response


def send_response(box_url, username, challenge_response):
    """ Send the response and return the parsed sid. raises an Exception on error """
    # Build response params
    post_data = {"username": username, "response": challenge_response}
    # post_data = urllib.parse.urlencode(post_data_dict).encode()
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    url = box_url + LOGIN_SID_ROUTE
    r = requests.post(url, headers=headers, data=post_data)
    # Parse SID from resulting XML.
    xml = etree.fromstring(r.content)
    return xml.find("SID").text


def get_page_content(server, session_id, page, port=80):
    """Fetches a page from the Fritzbox and returns its content

    :param server: the ip address of the Fritzbox
    :param session_id: a valid session id
    :param page: the page you are regquesting
    :param port: the port the Fritzbox webserver runs on
    :return: the content of the page
    """

    headers = {"Accept": "application/xml", "Content-Type": "text/plain", "User-Agent": USER_AGENT}

    url = "http://{}:{}/{}?sid={}".format(server, port, page, session_id)
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

    headers = {
        "Accept": "application/xml",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": USER_AGENT,
    }

    url = "http://{}:{}/data.lua".format(server, port)
    data = {"xhr": 1, "sid": session_id, "lang": "en", "page": page, "xhrId": "all", "no_sidrenew": ""}
    try:
        r = requests.post(url, data=data, headers=headers)
    except requests.exceptions.HTTPError as err:
        print(err)
        sys.exit(1)
    return r.content
