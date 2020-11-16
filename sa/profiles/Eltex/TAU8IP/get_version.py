# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.TAU8IP.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Python modules

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "Eltex.TAU8IP.get_version"
    cache = True
    interface = IGetVersion

    def execute(self):
        # tau8
        platform = self.cli("cat /tmp/board_type").strip()
        if "No such file or directory" in platform:
            #tau32
            platform = self.cli("cat /tmp/factory |grep type").split(":", 1)[1].strip()

        # tau8
        serial = self.cli("cat /tmp/board_serial").strip()
        if "No such file or directory" in serial:
            #tau32 or tau1m
            serial = self.cli("cat /tmp/factory |grep 'SN:'").split(":", 1)[1].strip()
            if "No such file or directory" in serial:
                #tau1m
                serial = self.cli("cat /tmp/.board_desc |grep 'Serial:'").split(":", 1)[1].strip()
        return {
            "vendor": "Eltex",
            "platform": platform,
            "version": self.cli("cat /version").strip(),
            "attributes": {"serial": serial}
        }