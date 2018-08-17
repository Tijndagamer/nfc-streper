#!/usr/bin/python2
"""
    nfc-streper.py

    Easily keep track of who drank how much beer by checking in each beer with
    your NFC ID tag.

    Copyright (c) 2018 Martijn

    nfc-streper is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    nfc-streper is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with nfc-streper.  If not, see <http://www.gnu.org/licenses/>.
"""

import nfc
import re
import sys

# Regexes
id_re = re.compile("ID=[0-9A-F]{8}")

registered_ids = {"7327A72E" : "Martijn"}

def get_id(tag):
    return id_re.findall(str(tag))[0].replace("ID=", '')

def on_startup(targets):
    for t in targets:
        t.sensf_req = bytearray.fromhex("0012FC0000")
    return targets

def on_connect(tag):
    t_id = get_id(tag)
    try:
        print("Registered tag! name: " + registered_ids[t_id])
    except KeyError:
        print("Unregistered ID.")
    print(get_id(tag))

rdwr_options = {
    "targets" : ["106A"],
    "on-startup" : on_startup,
    "on-connect" : on_connect,
}

with nfc.ContactlessFrontend("ttyAMA0") as clf:
    while True:
        try:
            tag = clf.connect(rdwr=rdwr_options)
        except KeyboardInterrupt:
            clf.close()
            sys.exit()
