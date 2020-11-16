# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Eltex.TAU.get_chassis_id
# ---------------------------------------------------------------------
# Copyright (C) 2007-2018 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.script.base import BaseScript
from noc.sa.interfaces.igetchassisid import IGetChassisID
from noc.core.mac import MAC


class Script(BaseScript):
    name = "Eltex.TAU.get_chassis_id"
    cache = True
    interface = IGetChassisID

    def execute(self):
        # tau8
        mac = self.cli("cat /tmp/board_mac").strip()
        if "No such file or directory" in mac:
            # tau32
            m = self.cli("cat /tmp/factory |grep MAC")
            mac = m.split(":", 1)[1].strip()
        return {"first_chassis_mac": MAC(mac), "last_chassis_mac": MAC(mac)}