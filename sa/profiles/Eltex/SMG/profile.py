# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Vendor: Eltex
# OS:     SMG
# ---------------------------------------------------------------------
# Copyright (C) 2007-2019 The NOC Project
# See LICENSE for details
# ---------------------------------------------------------------------

# NOC modules
from noc.core.profile.base import BaseProfile


class Profile(BaseProfile):
    name = "Eltex.SMG"
    #pattern_unprivileged_prompt = r"^\S+?>"
    pattern_prompt = r"(^\S+?>)|(/[\w/]+ # )"
    pattern_syntax_error = r"\^"
    command_exit = "exit"
