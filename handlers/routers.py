# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Object Classification Rules handlers
# ----------------------------------------------------------------------
# Copyright (C) 2007-2017 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
# import logging
# NOC modules
from noc.sa.models.managedobject import ManagedObject
from noc.sa.models.commandsnippet import CommandSnippet

#logger = logging.getLogger(name)

def handler(router_elder):
    cs = CommandSnippet.objects.get(name="TIK RB.TIK DHCP RELAY")
    for mo in ManagedObject.objects.filter(is_managed=True, administrative_domain="Роутеры"):
        try:
            conf = {"object": mo}
            cs.expand(conf)
        except:
            #router_elder.logger.info("Что-то пошло не так.")