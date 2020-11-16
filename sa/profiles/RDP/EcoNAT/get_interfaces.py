# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.TAU8IP.get_interfaces
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetinterfaces import IGetInterfaces
from noc.core.ip import IPv4


class Script(BaseScript):
    name = "Eltex.TAU8IP.get_interfaces"
    cache = True
    interface = IGetInterfaces

    rx_sh_int = re.compile(
        r"^(?P<ifname>\S+)\s+Link\sencap:(?P<itype>\S+)\s+"
        r"(?:HWaddr\s+(?P<mac>\S+)|Loopback)"
        r"(?P<ipv4sec>:?\s+inet\s+addr:(?P<ipv4>\S+)\s+(?:(|\S+\s+)(Mask:|\s+|/)(?P<maskv4>\S+))|)|"
        r"(?P<ipv6sec>\s+inet6\s+addr:\s+(?P<ipv6>\S+)/(?P<maskv6>\d+)\s+Scope:(?P<scopev6>\S+))|(.*)"
        r"\s+\S.+MTU:(?P<mtu>\S+)",
        re.MULTILINE | re.IGNORECASE,
    )

    INTERFACE_TYPES = {"local": "loopback", "ethernet": "physical"}  # Loopback

    @classmethod
    def get_interface_type(cls, name):
        c = cls.INTERFACE_TYPES.get(name.lower())
        return c

    def execute(self):
        interfaces = []
        v = self.cli("ifconfig", cached=True)
        for line in v.split("\n\n"):
            match = self.rx_sh_int.search(line)
            if match:
                ifname = match.group("ifname")
                itype = match.group("itype")
                iface = {
                    "type": self.get_interface_type(itype),
                    "name": ifname,
                    "admin_status": True,
                    "oper_status": True,
                    "subinterfaces": [
                        {
                            "name": ifname,
                            "mtu": match.group("mtu"),
                            "admin_status": True,
                            "oper_status": True,
                            "enabled_afi": ["BRIDGE"],
                        }
                    ],
                }
                if match.group("ipv4"):
                    ip_address = match.group("ipv4")
                    ip_subnet = match.group("maskv4")
                    ip_address = "%s/%s" % (ip_address, IPv4.netmask_to_len(ip_subnet))
                    ip_list = [ip_address]
                    enabled_afi = []
                    ip_interfaces = "ipv4_addresses"
                    enabled_afi += ["IPv4"]
                    iface["subinterfaces"][0]["enabled_afi"] = enabled_afi
                    iface["subinterfaces"][0][ip_interfaces] = ip_list
                if match.group("mac"):
                    mac = match.group("mac")
                    iface["mac"] = mac
                interfaces += [iface]
        return [{"interfaces": interfaces}]
