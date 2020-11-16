# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.ME.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Python modules
import re

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "Eltex.ME.get_version"
    cache = True
    interface = IGetVersion

    rx_serial = re.compile(
        r"Serial\s+number:\s+(?P<serial>\S+)\s+",
        re.MULTILINE | re.DOTALL,
    )
    rx_version = re.compile(
        r"System type:\s+Eltex\s+(?P<platform>\S+)"
        r".*\s+"
        r".*\s+"
        r"System software:.*version\s+(?P<version>\S+)",
        re.MULTILINE | re.DOTALL,
    )

    def execute_cli(self):
        ser = self.cli("show system inventory", cached=True)
        match_s = self.rx_serial.search(ser)

        ver = self.cli("show system", cached=True)
        match_v = self.rx_version.search(ver)

        return {
            "vendor": "Eltex",
            "platform": match_v.group("platform"),
            "version": match_v.group("version"),
            "attributes": {
                "serial": match_s.group("serial")
            }
        }
