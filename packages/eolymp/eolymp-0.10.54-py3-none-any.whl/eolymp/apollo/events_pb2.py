# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/apollo/events.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x65olymp/apollo/events.proto\x12\reolymp.apollo\"5\n\x0eStarAddedEvent\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\"7\n\x10StarRemovedEvent\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\tB/Z-github.com/eolymp/go-sdk/eolymp/apollo;apollob\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.apollo.events_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z-github.com/eolymp/go-sdk/eolymp/apollo;apollo'
  _STARADDEDEVENT._serialized_start=45
  _STARADDEDEVENT._serialized_end=98
  _STARREMOVEDEVENT._serialized_start=100
  _STARREMOVEDEVENT._serialized_end=155
# @@protoc_insertion_point(module_scope)
