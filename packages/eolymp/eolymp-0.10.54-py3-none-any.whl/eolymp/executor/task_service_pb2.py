# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/executor/task_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2
from eolymp.executor import evaluation_task_pb2 as eolymp_dot_executor_dot_evaluation__task__pb2
from eolymp.executor import generation_task_pb2 as eolymp_dot_executor_dot_generation__task__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"eolymp/executor/task_service.proto\x12\x0f\x65olymp.executor\x1a\"eolymp/annotations/ratelimit.proto\x1a%eolymp/executor/evaluation_task.proto\x1a%eolymp/executor/generation_task.proto\"\x87\x01\n\x0f\x43reateTaskInput\x12\x35\n\nevaluation\x18\x01 \x01(\x0b\x32\x1f.eolymp.executor.EvaluationTaskH\x00\x12\x35\n\ngeneration\x18\x02 \x01(\x0b\x32\x1f.eolymp.executor.GenerationTaskH\x00\x42\x06\n\x04task\"#\n\x10\x43reateTaskOutput\x12\x0f\n\x07task_id\x18\x01 \x01(\t2r\n\x0bTaskService\x12\x63\n\nCreateTask\x12 .eolymp.executor.CreateTaskInput\x1a!.eolymp.executor.CreateTaskOutput\"\x10\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xc8\x01\x42\x33Z1github.com/eolymp/go-sdk/eolymp/executor;executorb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.executor.task_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/executor;executor'
  _TASKSERVICE.methods_by_name['CreateTask']._options = None
  _TASKSERVICE.methods_by_name['CreateTask']._serialized_options = b'\352\342\n\014\365\342\n\000\000\240A\370\342\n\310\001'
  _CREATETASKINPUT._serialized_start=170
  _CREATETASKINPUT._serialized_end=305
  _CREATETASKOUTPUT._serialized_start=307
  _CREATETASKOUTPUT._serialized_end=342
  _TASKSERVICE._serialized_start=344
  _TASKSERVICE._serialized_end=458
# @@protoc_insertion_point(module_scope)
