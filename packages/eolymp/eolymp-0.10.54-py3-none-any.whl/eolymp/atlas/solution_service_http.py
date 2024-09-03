# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class SolutionServiceClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def CreateSolution(self, request, **kwargs):
        path = "/solutions"

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateSolutionOutput"),
            **kwargs,
        )

    def UpdateSolution(self, request, **kwargs):
        path = "/solutions/"+urllib.parse.quote(request.solution_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.solution_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateSolutionOutput"),
            **kwargs,
        )

    def DeleteSolution(self, request, **kwargs):
        path = "/solutions/"+urllib.parse.quote(request.solution_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.solution_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteSolutionOutput"),
            **kwargs,
        )

    def DescribeSolution(self, request, **kwargs):
        path = "/solutions/"+urllib.parse.quote(request.solution_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.solution_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeSolutionOutput"),
            **kwargs,
        )

    def ListSolutions(self, request, **kwargs):
        path = "/solutions"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListSolutionsOutput"),
            **kwargs,
        )

