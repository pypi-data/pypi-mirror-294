# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/executor/generation_task.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.executor import script_pb2 as eolymp_dot_executor_dot_script__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%eolymp/executor/generation_task.proto\x12\x0f\x65olymp.executor\x1a\x1c\x65olymp/executor/script.proto\"\xa6\x04\n\x0eGenerationTask\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\x12\x0e\n\x06origin\x18\x03 \x01(\t\x12\x31\n\x04runs\x18\n \x03(\x0b\x32#.eolymp.executor.GenerationTask.Run\x12(\n\x07scripts\x18\x14 \x03(\x0b\x32\x17.eolymp.executor.Script\x1a\x33\n\tGenerator\x12\x13\n\x0bscript_name\x18\x01 \x01(\t\x12\x11\n\targuments\x18\x02 \x03(\t\x1a\xcd\x02\n\x03Run\x12\x11\n\treference\x18\x01 \x01(\t\x12\x19\n\x0finput_object_id\x18\n \x01(\tH\x00\x12\x17\n\rinput_content\x18\x0b \x01(\tH\x00\x12\x13\n\tinput_url\x18\x0c \x01(\tH\x00\x12\x44\n\x0finput_generator\x18\r \x01(\x0b\x32).eolymp.executor.GenerationTask.GeneratorH\x00\x12\x1a\n\x10\x61nswer_object_id\x18\x14 \x01(\tH\x01\x12\x18\n\x0e\x61nswer_content\x18\x15 \x01(\tH\x01\x12\x14\n\nanswer_url\x18\x16 \x01(\tH\x01\x12\x45\n\x10\x61nswer_generator\x18\x17 \x01(\x0b\x32).eolymp.executor.GenerationTask.GeneratorH\x01\x42\x07\n\x05inputB\x08\n\x06\x61nswerB3Z1github.com/eolymp/go-sdk/eolymp/executor;executorb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.executor.generation_task_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/executor;executor'
  _GENERATIONTASK._serialized_start=89
  _GENERATIONTASK._serialized_end=639
  _GENERATIONTASK_GENERATOR._serialized_start=252
  _GENERATIONTASK_GENERATOR._serialized_end=303
  _GENERATIONTASK_RUN._serialized_start=306
  _GENERATIONTASK_RUN._serialized_end=639
# @@protoc_insertion_point(module_scope)
