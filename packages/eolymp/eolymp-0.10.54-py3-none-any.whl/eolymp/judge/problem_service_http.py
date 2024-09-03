# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class ProblemServiceClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def ImportProblem(self, request, **kwargs):
        path = "/problems"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ImportProblemOutput"),
            **kwargs,
        )

    def SyncProblem(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/sync"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.SyncProblemOutput"),
            **kwargs,
        )

    def UpdateProblem(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.UpdateProblemOutput"),
            **kwargs,
        )

    def ListProblems(self, request, **kwargs):
        path = "/problems"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListProblemsOutput"),
            **kwargs,
        )

    def DescribeProblem(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeProblemOutput"),
            **kwargs,
        )

    def DeleteProblem(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DeleteProblemOutput"),
            **kwargs,
        )

    def LookupCodeTemplate(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/lookup-template"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.LookupCodeTemplateOutput"),
            **kwargs,
        )

    def DescribeCodeTemplate(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/templates/"+urllib.parse.quote(request.template_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.template_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeCodeTemplateOutput"),
            **kwargs,
        )

    def ListStatements(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/statements"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListStatementsOutput"),
            **kwargs,
        )

    def ListAttachments(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/attachments"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListAttachmentsOutput"),
            **kwargs,
        )

    def ListExamples(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/examples"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListExamplesOutput"),
            **kwargs,
        )

