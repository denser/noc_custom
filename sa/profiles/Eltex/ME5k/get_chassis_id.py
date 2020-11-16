# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.ME.get_chassis_id
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID
from noc.core.mac import MAC


class Script(BaseScript):
    name = "Eltex.ME.get_chassis_id"
    cache = True
    interface = IGetChassisID

    rx_mac = re.compile(
            r"System MAC address:\s+(?P<mac>\S+)\s+",
            re.MULTILINE | re.DOTALL,
        )

    def execute_cli(self):
        mac = self.cli("show system")
        match = self.rx_mac.search(mac)
        mac = match.group("mac")

        return {"first_chassis_mac": MAC(mac), "last_chassis_mac": MAC(mac)}
