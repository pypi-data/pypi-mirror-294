# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class JudgeClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def CreateContest(self, request, **kwargs):
        path = "/contests"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.CreateContestOutput"),
            **kwargs,
        )

    def DeleteContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DeleteContestOutput"),
            **kwargs,
        )

    def UpdateContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.UpdateContestOutput"),
            **kwargs,
        )

    def DescribeContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeContestOutput"),
            **kwargs,
        )

    def ListContests(self, request, **kwargs):
        path = "/contests"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListContestsOutput"),
            **kwargs,
        )

    def OpenContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/open"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.OpenContestOutput"),
            **kwargs,
        )

    def CloseContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/close"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.CloseContestOutput"),
            **kwargs,
        )

    def SuspendContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/suspend"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.SuspendContestOutput"),
            **kwargs,
        )

    def FreezeContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/freeze"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.FreezeContestOutput"),
            **kwargs,
        )

    def ResumeContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/resume"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ResumeContestOutput"),
            **kwargs,
        )

    def ImportProblem(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ImportProblemOutput"),
            **kwargs,
        )

    def SyncProblem(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/sync"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.SyncProblemOutput"),
            **kwargs,
        )

    def UpdateProblem(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.UpdateProblemOutput"),
            **kwargs,
        )

    def ListProblems(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListProblemsOutput"),
            **kwargs,
        )

    def DescribeProblem(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeProblemOutput"),
            **kwargs,
        )

    def DescribeCodeTemplate(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/templates/"+urllib.parse.quote(request.template_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""
        request.template_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeCodeTemplateOutput"),
            **kwargs,
        )

    def LookupCodeTemplate(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/lookup-template"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.LookupCodeTemplateOutput"),
            **kwargs,
        )

    def ListStatements(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/statements"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListStatementsOutput"),
            **kwargs,
        )

    def ListAttachments(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/attachments"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListAttachmentsOutput"),
            **kwargs,
        )

    def ListExamples(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/examples"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListExamplesOutput"),
            **kwargs,
        )

    def DeleteProblem(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DeleteProblemOutput"),
            **kwargs,
        )

    def RetestProblem(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/retest"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.RetestProblemOutput"),
            **kwargs,
        )

    def AddParticipant(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.AddParticipantOutput"),
            **kwargs,
        )

    def EnableParticipant(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/enable"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.EnableParticipantOutput"),
            **kwargs,
        )

    def DisableParticipant(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/disable"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DisableParticipantOutput"),
            **kwargs,
        )

    def UpdateParticipant(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.UpdateParticipantOutput"),
            **kwargs,
        )

    def RemoveParticipant(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.RemoveParticipantOutput"),
            **kwargs,
        )

    def ListParticipants(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListParticipantsOutput"),
            **kwargs,
        )

    def DescribeParticipant(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeParticipantOutput"),
            **kwargs,
        )

    def IntrospectParticipant(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/introspect"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.IntrospectParticipantOutput"),
            **kwargs,
        )

    def JoinContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/join"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.JoinContestOutput"),
            **kwargs,
        )

    def StartContest(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/start"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.StartContestOutput"),
            **kwargs,
        )

    def VerifyPasscode(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/verify-passcode"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.VerifyPasscodeOutput"),
            **kwargs,
        )

    def EnterPasscode(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/enter-passcode"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.EnterPasscodeOutput"),
            **kwargs,
        )

    def ResetPasscode(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/passcode"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ResetPasscodeOutput"),
            **kwargs,
        )

    def SetPasscode(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/passcode"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="PUT",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.SetPasscodeOutput"),
            **kwargs,
        )

    def RemovePasscode(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/passcode"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.RemovePasscodeOutput"),
            **kwargs,
        )

    def CreateSubmission(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/problems/"+urllib.parse.quote(request.problem_id)+"/submissions"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.problem_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.CreateSubmissionOutput"),
            **kwargs,
        )

    def ListSubmissions(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/submissions"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListSubmissionsOutput"),
            **kwargs,
        )

    def DescribeSubmission(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/submissions/"+urllib.parse.quote(request.submission_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.submission_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeSubmissionOutput"),
            **kwargs,
        )

    def RetestSubmission(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/submissions/"+urllib.parse.quote(request.submission_id)+"/retest"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.submission_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.RetestSubmissionOutput"),
            **kwargs,
        )

    def DeleteSubmission(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/submissions/"+urllib.parse.quote(request.submission_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.submission_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DeleteSubmissionOutput"),
            **kwargs,
        )

    def RestoreSubmission(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/submissions/"+urllib.parse.quote(request.submission_id)+"/restore"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.submission_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.RestoreSubmissionOutput"),
            **kwargs,
        )

    def CreateAnnouncement(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/announcements"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.CreateAnnouncementOutput"),
            **kwargs,
        )

    def UpdateAnnouncement(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/announcements/"+urllib.parse.quote(request.announcement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.announcement_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.UpdateAnnouncementOutput"),
            **kwargs,
        )

    def DeleteAnnouncement(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/announcements/"+urllib.parse.quote(request.announcement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.announcement_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DeleteAnnouncementOutput"),
            **kwargs,
        )

    def ReadAnnouncement(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/announcements/"+urllib.parse.quote(request.announcement_id)+"/read"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.announcement_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ReadAnnouncementOutput"),
            **kwargs,
        )

    def DescribeAnnouncement(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/announcements/"+urllib.parse.quote(request.announcement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.announcement_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeAnnouncementOutput"),
            **kwargs,
        )

    def DescribeAnnouncementStatus(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/announcements/"+urllib.parse.quote(request.announcement_id)+"/status"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.announcement_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeAnnouncementStatusOutput"),
            **kwargs,
        )

    def ListAnnouncements(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/announcements"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListAnnouncementsOutput"),
            **kwargs,
        )

    def IntrospectScore(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/introspect/score"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.IntrospectScoreOutput"),
            **kwargs,
        )

    def DescribeScore(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/score"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeScoreOutput"),
            **kwargs,
        )

    def ImportScore(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/scores"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ImportScoreOutput"),
            **kwargs,
        )

    def ExportScore(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/participants/"+urllib.parse.quote(request.participant_id)+"/scores"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""
        request.participant_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ExportScoreOutput"),
            **kwargs,
        )

    def ListResult(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/results"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListResultOutput"),
            **kwargs,
        )

    def RebuildScore(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/rebuild"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.RebuildScoreOutput"),
            **kwargs,
        )

    def ListActivities(self, request, **kwargs):
        path = "/contests/"+urllib.parse.quote(request.contest_id)+"/activities"

        # Cleanup URL parameters to avoid any ambiguity
        request.contest_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListActivitiesOutput"),
            **kwargs,
        )

    def DescribeContestUsage(self, request, **kwargs):
        path = "/usage/contests"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeContestUsageOutput"),
            **kwargs,
        )

