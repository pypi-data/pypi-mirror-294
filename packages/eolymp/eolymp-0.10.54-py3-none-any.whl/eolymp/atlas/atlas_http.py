# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class AtlasClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def CreateProblem(self, request, **kwargs):
        path = "/problems"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateProblemOutput"),
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
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteProblemOutput"),
            **kwargs,
        )

    def ListProblems(self, request, **kwargs):
        path = "/problems"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListProblemsOutput"),
            **kwargs,
        )

    def VoteProblem(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/vote"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.VoteProblemOutput"),
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
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeProblemOutput"),
            **kwargs,
        )

    def UpdateProblem(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateProblemOutput"),
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
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.SyncProblemOutput"),
            **kwargs,
        )

    def SetBookmark(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/bookmark"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.SetBookmarkOutput"),
            **kwargs,
        )

    def GetBookmark(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/bookmark"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.GetBookmarkOutput"),
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
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListExamplesOutput"),
            **kwargs,
        )

    def UpdateTestingConfig(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testing"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateTestingConfigOutput"),
            **kwargs,
        )

    def DescribeTestingConfig(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testing"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeTestingConfigOutput"),
            **kwargs,
        )

    def UpdateChecker(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/checker"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateCheckerOutput"),
            **kwargs,
        )

    def DescribeChecker(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/checker"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeCheckerOutput"),
            **kwargs,
        )

    def UpdateInteractor(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/interactor"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateInteractorOutput"),
            **kwargs,
        )

    def DescribeInteractor(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/interactor"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeInteractorOutput"),
            **kwargs,
        )

    def CreateStatement(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/statements"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateStatementOutput"),
            **kwargs,
        )

    def UpdateStatement(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/statements/"+urllib.parse.quote(request.statement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.statement_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateStatementOutput"),
            **kwargs,
        )

    def DeleteStatement(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/statements/"+urllib.parse.quote(request.statement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.statement_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteStatementOutput"),
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
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListStatementsOutput"),
            **kwargs,
        )

    def DescribeStatement(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/statements/"+urllib.parse.quote(request.statement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.statement_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeStatementOutput"),
            **kwargs,
        )

    def LookupStatement(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/translate"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.LookupStatementOutput"),
            **kwargs,
        )

    def PreviewStatement(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/renders"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.PreviewStatementOutput"),
            **kwargs,
        )

    def CreateTestset(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateTestsetOutput"),
            **kwargs,
        )

    def UpdateTestset(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateTestsetOutput"),
            **kwargs,
        )

    def DeleteTestset(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteTestsetOutput"),
            **kwargs,
        )

    def ListTestsets(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListTestsetsOutput"),
            **kwargs,
        )

    def DescribeTestset(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeTestsetOutput"),
            **kwargs,
        )

    def CreateTest(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)+"/tests"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateTestOutput"),
            **kwargs,
        )

    def UpdateTest(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)+"/tests/"+urllib.parse.quote(request.test_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""
        request.test_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateTestOutput"),
            **kwargs,
        )

    def DeleteTest(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)+"/tests/"+urllib.parse.quote(request.test_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""
        request.test_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteTestOutput"),
            **kwargs,
        )

    def ListTests(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)+"/tests"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListTestsOutput"),
            **kwargs,
        )

    def DescribeTest(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/testsets/"+urllib.parse.quote(request.testset_id)+"/tests/"+urllib.parse.quote(request.test_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.testset_id = ""
        request.test_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeTestOutput"),
            **kwargs,
        )

    def CreateCodeTemplate(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/templates"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateCodeTemplateOutput"),
            **kwargs,
        )

    def UpdateCodeTemplate(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/templates/"+urllib.parse.quote(request.template_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.template_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateCodeTemplateOutput"),
            **kwargs,
        )

    def DeleteCodeTemplate(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/templates/"+urllib.parse.quote(request.template_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.template_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteCodeTemplateOutput"),
            **kwargs,
        )

    def ListCodeTemplates(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/templates"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListCodeTemplatesOutput"),
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
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeCodeTemplateOutput"),
            **kwargs,
        )

    def LookupCodeTemplate(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/template"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.LookupCodeTemplateOutput"),
            **kwargs,
        )

    def CreateAttachment(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/attachments"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateAttachmentOutput"),
            **kwargs,
        )

    def UpdateAttachment(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/attachments/"+urllib.parse.quote(request.attachment_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.attachment_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.UpdateAttachmentOutput"),
            **kwargs,
        )

    def DeleteAttachment(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/attachments/"+urllib.parse.quote(request.attachment_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.attachment_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DeleteAttachmentOutput"),
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
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListAttachmentsOutput"),
            **kwargs,
        )

    def DescribeAttachment(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/attachments/"+urllib.parse.quote(request.attachment_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.attachment_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeAttachmentOutput"),
            **kwargs,
        )

    def ListVersions(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/versions"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListVersionsOutput"),
            **kwargs,
        )

    def ListProblemTop(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/top"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListProblemTopOutput"),
            **kwargs,
        )

    def DescribeProblemGrading(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/grading"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeProblemGradingOutput"),
            **kwargs,
        )

    def CreateSubmission(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/submissions"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.CreateSubmissionOutput"),
            **kwargs,
        )

    def DescribeSubmission(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/submissions/"+urllib.parse.quote(request.submission_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.submission_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeSubmissionOutput"),
            **kwargs,
        )

    def RetestSubmission(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/submissions/"+urllib.parse.quote(request.submission_id)+"/retest"

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.submission_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.RetestSubmissionOutput"),
            **kwargs,
        )

    def ListSubmissions(self, request, **kwargs):
        path = "/submissions"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.ListSubmissionsOutput"),
            **kwargs,
        )

    def DescribeScore(self, request, **kwargs):
        path = "/problems/"+urllib.parse.quote(request.problem_id)+"/scores/"+urllib.parse.quote(request.member_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.problem_id = ""
        request.member_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.atlas.DescribeScoreOutput"),
            **kwargs,
        )

