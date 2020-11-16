# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: ZTE
# OS:     ZXR10
# ---------------------------------------------------------------------
# Copyright (C) 2007-2011 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------
"""
"""
# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "ZTE.ZXR10-2826S"
    pattern_more = [
        (r"^----- more ----- Press Q or Ctrl\+C to break -----$", " "),
        #(r"The current configuration will be written to the device. Are you sure? [Y/N]:", "Y"),
        #(r"(To leave the existing filename unchanged, press the enter key):", "\n"),
        #(r"flash:/startup.cfg exists, overwrite? [Y/N]:", "Y"),
    ]
    #command_more = "\r\n"


    pattern_unprivileged_prompt = r"^\S+?>"
    pattern_syntax_error = r"Command not found"
#    command_disable_pager = "terminal length 0"
    command_super = "enable"
#    command_enter_config = "configure terminal"
#    command_leave_config = "exit"
    command_save_config = "saveconfig\n"
    pattern_prompt = r"^(?P<hostname>\S+?)(?:-\d+)?(?:\(cfg[^\)]*\))?#"
    requires_netmask_conversion = True
    convert_mac = BaseProfile.convert_mac_to_cisco
    config_volatile = [
        (r"^ntp clock-period .*?^"),
        (r"^\s+"),
    ]
    telnet_naws = "\x7f\x7f\x7f\x7f"
