# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: Eltex
# OS:     TAU8IP
# ---------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Eltex.TAU8IP"
    pattern_username = "^\S+ [Ll]ogin:"
    pattern_password = "^[Pp]assword:"
    pattern_prompt = r"^\S+@(?P<hostname>\S+?):.+((#)|(])|(\$))"
    command_exit = "exit"