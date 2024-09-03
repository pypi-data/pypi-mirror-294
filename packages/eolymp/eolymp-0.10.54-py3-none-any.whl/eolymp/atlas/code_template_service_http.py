# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class CodeTemplateServiceClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def CreateCodeTemplate(self, request, **kwargs):
        path = "/templates"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateCodeTemplateOutput"),
            **kwargs,
        )

    def UpdateCodeTemplate(self, request, **kwargs):
        path = "/templates/"+urllib.parse.quote(request.template_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.template_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateCodeTemplateOutput"),
            **kwargs,
        )

    def DeleteCodeTemplate(self, request, **kwargs):
        path = "/templates/"+urllib.parse.quote(request.template_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.template_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteCodeTemplateOutput"),
            **kwargs,
        )

    def ListCodeTemplates(self, request, **kwargs):
        path = "/templates"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListCodeTemplatesOutput"),
            **kwargs,
        )

    def DescribeCodeTemplate(self, request, **kwargs):
        path = "/templates/"+urllib.parse.quote(request.template_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.template_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeCodeTemplateOutput"),
            **kwargs,
        )

    def LookupCodeTemplate(self, request, **kwargs):
        path = "/template"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.LookupCodeTemplateOutput"),
            **kwargs,
        )

