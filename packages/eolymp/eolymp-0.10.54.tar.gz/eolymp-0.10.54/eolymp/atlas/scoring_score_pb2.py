# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/atlas/scoring_score.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n eolymp/atlas/scoring_score.proto\x12\x0c\x65olymp.atlas\x1a\x1fgoogle/protobuf/timestamp.proto\"\x9b\x01\n\x05Score\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nproblem_id\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12\x11\n\tmember_id\x18\x07 \x01(\t\x12-\n\tsolved_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05score\x18\x05 \x01(\x02\x12\x10\n\x08\x61ttempts\x18\x08 \x01(\rB-Z+github.com/eolymp/go-sdk/eolymp/atlas;atlasb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.atlas.scoring_score_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z+github.com/eolymp/go-sdk/eolymp/atlas;atlas'
  _SCORE._serialized_start=84
  _SCORE._serialized_end=239
# @@protoc_insertion_point(module_scope)
