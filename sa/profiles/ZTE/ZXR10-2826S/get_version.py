# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# ZTE.ZXR10-2826S.get_version
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# Python modules
import re

# re modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetversion import IGetVersion


class Script(BaseScript):
    name = "ZTE.ZXR10-2826S.get_version"
    cache = True
    interface = IGetVersion

    rx_ver = re.compile(
        r"^.*Version [Nn]umber\s+:.+(?P<version>V\S+)$",
        re.MULTILINE | re.DOTALL,
    )
    rx_module0 = re.compile(
        r"^.*Module 0:\s+(?P<platform>.+?);",
        re.MULTILINE | re.DOTALL,
    )
    rx_module1 = re.compile(
        r"^.*Module 1:\s+(?P<module>.+?);",
        re.MULTILINE | re.DOTALL,
    )

    def execute_cli(self):
        try:
           v = self.cli("version")
        except self.CLISyntaxError:
           v = self.cli("show version")
        version = self.rx_ver.search(v)
        platform = self.rx_module0.search(v)
        platform = platform.group("platform")
        module = self.rx_module1.search(v)
        if module:
            module = module.group("module")
        else:
            module = "N/A"
        if platform.startswith("ZXR10 "):
            platform = platform[6:]
        return {"vendor": "ZTE", "platform": platform, "version": version.group("version"), "module": module}
