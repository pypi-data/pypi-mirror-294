# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/executor/checker.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.executor import file_pb2 as eolymp_dot_executor_dot_file__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x65olymp/executor/checker.proto\x12\x0f\x65olymp.executor\x1a\x1a\x65olymp/executor/file.proto\"\xbf\x02\n\x07\x43hecker\x12+\n\x04type\x18\x01 \x01(\x0e\x32\x1d.eolymp.executor.Checker.Type\x12\x0c\n\x04lang\x18\x02 \x01(\t\x12\x0e\n\x06source\x18\x03 \x01(\t\x12\x12\n\nsource_url\x18\x08 \x01(\t\x12\x11\n\tprecision\x18\x04 \x01(\x05\x12\x16\n\x0e\x63\x61se_sensitive\x18\x05 \x01(\x08\x12\x17\n\x0forder_sensitive\x18\x06 \x01(\x08\x12\x0e\n\x06secret\x18\x07 \x01(\x08\x12$\n\x05\x66iles\x18\n \x03(\x0b\x32\x15.eolymp.executor.File\"[\n\x04Type\x12\x08\n\x04NONE\x10\x00\x12\n\n\x06TOKENS\x10\x01\x12\t\n\x05LINES\x10\x02\x12\x0b\n\x07PROGRAM\x10\x03\x12\x12\n\x0eLEGACY_PROGRAM\x10\x04\x12\x11\n\rQUERY_RESULTS\x10\x05\x42\x33Z1github.com/eolymp/go-sdk/eolymp/executor;executorb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.executor.checker_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/executor;executor'
  _CHECKER._serialized_start=79
  _CHECKER._serialized_end=398
  _CHECKER_TYPE._serialized_start=307
  _CHECKER_TYPE._serialized_end=398
# @@protoc_insertion_point(module_scope)
