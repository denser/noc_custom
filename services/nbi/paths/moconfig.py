# ----------------------------------------------------------------------
# moconfig API
# ----------------------------------------------------------------------
# Copyright (C) 2007-2022 The NOC Project
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
from fastapi import APIRouter, Path, Header, HTTPException
from fastapi.responses import PlainTextResponse

# NOC modules
from noc.sa.models.managedobject import ManagedObject
from noc.services.nbi.base import NBIAPI, API_ACCESS_HEADER, FORBIDDEN_MESSAGE

router = APIRouter()


class MoConfigAPI(NBIAPI):
    api_name = "moconfig"
    openapi_tags = ["moconfig API"]

    def get_routes(self):
        route_moconfig = {
            "path": "/api/nbi/moconfig/{address}",
            "method": "GET",
            "endpoint": self.handler_moconfig,
            "response_class": PlainTextResponse,
            "response_model": None,
            "name": "moconfig",
            "description": "Get last configuration for Managed Object with ip `address`",
        }
        route_moconfig_revision = {
            "path": "/api/nbi/moconfig/{address}/{revision}",
            "method": "GET",
            "endpoint": self.handler_moconfig_revision,
            "response_class": PlainTextResponse,
            "response_model": None,
            "name": "moconfig_revision",
            "description": "Get configuration revision `revision_id` for Managed Object with ip `address`",
        }
        return [route_moconfig, route_moconfig_revision]

    def _handler(self, access_header, address, revision=None):
        if not self.access_granted(access_header):
            raise HTTPException(403, FORBIDDEN_MESSAGE)
        mo = ManagedObject.objects.filter(address=address)[:1]
        if not mo:
            raise HTTPException(404, "Not Found {address}")
        if revision:
            if not mo[0].config.has_revision(revision):
                raise HTTPException(404, "Revision {revision} not found")
            moconfig = mo[0].config.get_revision(revision)
        else:
            moconfig = mo[0].config.read()
        if moconfig is None:
            raise HTTPException(204, "")
        return moconfig

    async def handler_moconfig(
        self, address: str, access_header: str = Header(..., alias=API_ACCESS_HEADER)
    ):
        return self._handler(access_header, address)

    async def handler_moconfig_revision(
        self,
        address: str,
        revision: str = Path(..., regex="^[0-9a-f]{24}$"),
        access_header: str = Header(..., alias=API_ACCESS_HEADER),
    ):
        return self._handler(access_header, address, revision)


# Install router
MoConfigAPI(router)
