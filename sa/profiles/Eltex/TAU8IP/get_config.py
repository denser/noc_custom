# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.TAU8IP.get_config
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetconfig import IGetConfig


class Script(BaseScript):
    name = "Eltex.TAU8IP.get_config"
    interface = IGetConfig

    def execute_cli(self, **kwargs):
        show = self.cli("find /tmp/etc/config/ -name '*' -print -exec cat {} \; 2>/dev/null")
        if "find /tmp/etc/config/" in show:
            # tau1m
            show = self.cli("cat /etc/config/cfg.yaml")
        return self.cleaned_config(show)
