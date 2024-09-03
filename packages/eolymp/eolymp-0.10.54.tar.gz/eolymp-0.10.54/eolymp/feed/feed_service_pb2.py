# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/feed/feed_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import http_pb2 as eolymp_dot_annotations_dot_http__pb2
from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2
from eolymp.feed import entry_pb2 as eolymp_dot_feed_dot_entry__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x65olymp/feed/feed_service.proto\x12\x0b\x65olymp.feed\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x17\x65olymp/feed/entry.proto\"/\n\x10ListEntriesInput\x12\x0c\n\x04size\x18\x0b \x01(\x05\x12\r\n\x05\x61\x66ter\x18\x0c \x01(\t\"_\n\x11ListEntriesOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12!\n\x05items\x18\x02 \x03(\x0b\x32\x12.eolymp.feed.Entry\x12\x18\n\x10next_page_cursor\x18\x03 \x01(\t2y\n\x0b\x46\x65\x65\x64Service\x12j\n\x0bListEntries\x12\x1d.eolymp.feed.ListEntriesInput\x1a\x1e.eolymp.feed.ListEntriesOutput\"\x1c\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n\x14\x82\xd3\xe4\x93\x02\x07\x12\x05/feedB+Z)github.com/eolymp/go-sdk/eolymp/feed;feedb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.feed.feed_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z)github.com/eolymp/go-sdk/eolymp/feed;feed'
  _FEEDSERVICE.methods_by_name['ListEntries']._options = None
  _FEEDSERVICE.methods_by_name['ListEntries']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240@\370\342\n\024\202\323\344\223\002\007\022\005/feed'
  _LISTENTRIESINPUT._serialized_start=139
  _LISTENTRIESINPUT._serialized_end=186
  _LISTENTRIESOUTPUT._serialized_start=188
  _LISTENTRIESOUTPUT._serialized_end=283
  _FEEDSERVICE._serialized_start=285
  _FEEDSERVICE._serialized_end=406
# @@protoc_insertion_point(module_scope)
