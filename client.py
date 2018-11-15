#!/usr/bin/env python
# encoding: utf-8
import socket
import fcntl
import struct
import uuid
import requests
import datetime
from __future__ import print_function

from config import AUTH, Ethernet, URL


def get_ip_address(ethernet):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ethernet[:15])
    )[20:24])


def get_mac_address():
    node = uuid.getnode()
    return uuid.UUID(int=node).hex[-12:]


if __name__ == "__main__":
    mac_address = get_mac_address()
    data = {
        "auth": AUTH,
        "client_id": mac_address,
        "data": {
            "ip": get_ip_address(Ethernet),
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }
    print(data)
    requests.post(url=URL, data=data)
