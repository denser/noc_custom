# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: RDP
# OS:     EcoNAT
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "RDP.EcoNAT"
#    command_more = "\r\n"
    command_submit = "\r"
#    pattern_unprivileged_prompt = r"^\S*>"
#    rogue_chars = ("\x1b[39m", "\x1b[3g", "\x1b[6n")
#    rogue_chars = [
#        ("\x1b[39m"),
#        ("\x1b[3g"),
#        ("\x1b[6n"),
#    ]
#    command_enter_config = "configure"
#    command_leave_config = "exit"
#    command_save_config = "apply; wr"
#    command_super = "configure"
#    pattern_username = "^\S+ [Ll]ogin:"
#    pattern_password = "^[Pp]assword:"
#    pattern_unprivileged_prompt = r"^\S+?>"
#    pattern_prompt = r"^\S+?>"
#    pattern_prompt = r"^\S+?>"
#    command_exit = "exit"
#    telnet_naws = "\x7f\x7f\x7f\x7f"
#    pattern_syntax_error = r"Unable to autocomplete - variants are not available"