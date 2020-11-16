# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# RDP.EcoNAT.get_version
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
    name = "RDP.EcoNAT.get_version"
    cache = True
    interface = IGetVersion

    rx = re.compile(
        r"^(?P<platform>.*)\s+\(C\).*\s+"
        r"Firmware version: (?P<version>\S+)\s+"
        r"S\/N: (?P<serial>\S+)$",
        re.MULTILINE | re.DOTALL,
    )

    def execute_cli(self):
        # 2020
        #self.cli("\n")
        v = self.cli("show version")
        match = self.rx.search(v)
        version = match.group('version')
        platform = match.group('platform')
        serial = match.group('serial')
        
        return {
            "vendor": "RDP",
            "platform": platform,
            "version": version,
            "attributes": {"serial": serial}
        }