# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler. DO NOT EDIT!
# See https://github.com/eolymp/contracts/tree/main/cmd/protoc-gen-python-esdk for more details.
"""Generated protocol buffer code."""

import urllib.parse
from google.protobuf import symbol_database as _symbol_database

_sym_db = _symbol_database.Default()


class AnnouncementServiceClient:
    def __init__(self, transport, url="https://api.eolymp.com"):
        self.transport = transport
        self.url = url

    def CreateAnnouncement(self, request, **kwargs):
        path = "/announcements"

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.CreateAnnouncementOutput"),
            **kwargs,
        )

    def UpdateAnnouncement(self, request, **kwargs):
        path = "/announcements/"+urllib.parse.quote(request.announcement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.announcement_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.UpdateAnnouncementOutput"),
            **kwargs,
        )

    def DeleteAnnouncement(self, request, **kwargs):
        path = "/announcements/"+urllib.parse.quote(request.announcement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.announcement_id = ""

        return self.transport.request(
            method="DELETE",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DeleteAnnouncementOutput"),
            **kwargs,
        )

    def ReadAnnouncement(self, request, **kwargs):
        path = "/announcements/"+urllib.parse.quote(request.announcement_id)+"/read"

        # Cleanup URL parameters to avoid any ambiguity
        request.announcement_id = ""

        return self.transport.request(
            method="POST",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ReadAnnouncementOutput"),
            **kwargs,
        )

    def DescribeAnnouncement(self, request, **kwargs):
        path = "/announcements/"+urllib.parse.quote(request.announcement_id)

        # Cleanup URL parameters to avoid any ambiguity
        request.announcement_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeAnnouncementOutput"),
            **kwargs,
        )

    def DescribeAnnouncementStatus(self, request, **kwargs):
        path = "/announcements/"+urllib.parse.quote(request.announcement_id)+"/status"

        # Cleanup URL parameters to avoid any ambiguity
        request.announcement_id = ""

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.DescribeAnnouncementStatusOutput"),
            **kwargs,
        )

    def ListAnnouncements(self, request, **kwargs):
        path = "/announcements"

        return self.transport.request(
            method="GET",
            url=self.url+path,
            request_data=request,
            response_symbol=_sym_db.GetSymbol("eolymp.judge.ListAnnouncementsOutput"),
            **kwargs,
        )

