# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class PlaygroundClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def CreateRun(self, request, **kwargs):
        path = "/runs"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.playground.CreateRunOutput"),
            **kwargs,
        )

    def DescribeRun(self, request, **kwargs):
        path = "/runs/"+urllib.parse.quote(request.run_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.run_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.playground.DescribeRunOutput"),
            **kwargs,
        )

    def WatchRun(self, request, **kwargs):
        path = "/runs/"+urllib.parse.quote(request.run_id)+"/watch"

        # Cleanup URL parameters to avoid any ambiguity
        request.run_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.playground.WatchRunOutput"),
            **kwargs,
        )

