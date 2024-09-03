# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class ScoreServiceClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def IntrospectScore(self, request, **kwargs):
        path = "/introspect/score"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.IntrospectScoreOutput"),
            **kwargs,
        )

    def DescribeScore(self, request, **kwargs):
        path = "/participants/"+urllib.parse.quote(request.participant_id)+"/score"

        # Cleanup URL parameters to avoid any ambiguity
        request.participant_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeScoreOutput"),
            **kwargs,
        )

    def ImportScore(self, request, **kwargs):
        path = "/participants/"+urllib.parse.quote(request.participant_id)+"/scores"

        # Cleanup URL parameters to avoid any ambiguity
        request.participant_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ImportScoreOutput"),
            **kwargs,
        )

    def ExportScore(self, request, **kwargs):
        path = "/participants/"+urllib.parse.quote(request.participant_id)+"/scores"

        # Cleanup URL parameters to avoid any ambiguity
        request.participant_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ExportScoreOutput"),
            **kwargs,
        )

    def ListResult(self, request, **kwargs):
        path = "/results"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListResultOutput"),
            **kwargs,
        )

    def ExportResult(self, request, **kwargs):
        path = "/results-export"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ExportResultOutput"),
            **kwargs,
        )

    def RebuildScore(self, request, **kwargs):
        path = "/rebuild"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.RebuildScoreOutput"),
            **kwargs,
        )

