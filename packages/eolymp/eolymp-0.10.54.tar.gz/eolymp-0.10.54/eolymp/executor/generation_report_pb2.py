# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/executor/generation_report.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.executor import stats_pb2 as eolymp_dot_executor_dot_stats__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'eolymp/executor/generation_report.proto\x12\x0f\x65olymp.executor\x1a\x1b\x65olymp/executor/stats.proto\"\xc3\x03\n\x10GenerationReport\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\x12\x0e\n\x06origin\x18\x03 \x01(\t\x12\r\n\x05\x61gent\x18\x04 \x01(\t\x12\r\n\x05\x65rror\x18\x14 \x01(\t\x12\x33\n\x04runs\x18( \x03(\x0b\x32%.eolymp.executor.GenerationReport.Run\x1a\xa7\x02\n\x03Run\x12\x11\n\treference\x18\x01 \x01(\t\x12<\n\x06status\x18\x02 \x01(\x0e\x32,.eolymp.executor.GenerationReport.Run.Status\x12\x11\n\tinput_url\x18\n \x01(\t\x12\x12\n\nanswer_url\x18\x0b \x01(\t\x12\x35\n\x15input_generator_stats\x18\x14 \x01(\x0b\x32\x16.eolymp.executor.Stats\x12\x36\n\x16\x61nswer_generator_stats\x18\x1e \x01(\x0b\x32\x16.eolymp.executor.Stats\"9\n\x06Status\x12\x08\n\x04NONE\x10\x00\x12\x0b\n\x07PENDING\x10\x01\x12\x0c\n\x08\x43OMPLETE\x10\x02\x12\n\n\x06\x46\x41ILED\x10\x03\x42\x33Z1github.com/eolymp/go-sdk/eolymp/executor;executorb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.executor.generation_report_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/executor;executor'
  _GENERATIONREPORT._serialized_start=90
  _GENERATIONREPORT._serialized_end=541
  _GENERATIONREPORT_RUN._serialized_start=246
  _GENERATIONREPORT_RUN._serialized_end=541
  _GENERATIONREPORT_RUN_STATUS._serialized_start=484
  _GENERATIONREPORT_RUN_STATUS._serialized_end=541
# @@protoc_insertion_point(module_scope)
