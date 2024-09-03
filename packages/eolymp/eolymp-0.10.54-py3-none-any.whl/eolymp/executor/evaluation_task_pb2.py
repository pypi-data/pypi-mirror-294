# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/executor/evaluation_task.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.executor import checker_pb2 as eolymp_dot_executor_dot_checker__pb2
from eolymp.executor import file_pb2 as eolymp_dot_executor_dot_file__pb2
from eolymp.executor import interactor_pb2 as eolymp_dot_executor_dot_interactor__pb2
from eolymp.executor import script_pb2 as eolymp_dot_executor_dot_script__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%eolymp/executor/evaluation_task.proto\x12\x0f\x65olymp.executor\x1a\x1d\x65olymp/executor/checker.proto\x1a\x1a\x65olymp/executor/file.proto\x1a eolymp/executor/interactor.proto\x1a\x1c\x65olymp/executor/script.proto\"\x8a\n\n\x0e\x45valuationTask\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x11\n\treference\x18\x02 \x01(\t\x12\x0e\n\x06origin\x18\x03 \x01(\t\x12\x10\n\x08priority\x18\x04 \x01(\r\x12\x0f\n\x07runtime\x18\n \x01(\t\x12\x0e\n\x06source\x18\x0b \x01(\t\x12\x12\n\nsource_url\x18n \x01(\t\x12\x12\n\nheader_url\x18o \x01(\t\x12\x12\n\nfooter_url\x18p \x01(\t\x12!\n\x19redirect_stderr_to_stdout\x18\r \x01(\x08\x12\x11\n\trun_count\x18\x10 \x01(\r\x12\x43\n\rpreconditions\x18( \x03(\x0b\x32,.eolymp.executor.EvaluationTask.Precondition\x12?\n\x0b\x63onstraints\x18\x14 \x03(\x0b\x32*.eolymp.executor.EvaluationTask.Constraint\x12)\n\x07\x63hecker\x18\x18 \x01(\x0b\x32\x18.eolymp.executor.Checker\x12/\n\ninteractor\x18\x19 \x01(\x0b\x32\x1b.eolymp.executor.Interactor\x12\x31\n\x04runs\x18\x1e \x03(\x0b\x32#.eolymp.executor.EvaluationTask.Run\x12$\n\x05\x66iles\x18\x32 \x03(\x0b\x32\x15.eolymp.executor.File\x12(\n\x07scripts\x18< \x03(\x0b\x32\x17.eolymp.executor.Script\x1a\x33\n\tGenerator\x12\x13\n\x0bscript_name\x18\x01 \x01(\t\x12\x11\n\targuments\x18\x02 \x03(\t\x1a\x89\x03\n\x03Run\x12\x11\n\treference\x18\x01 \x01(\t\x12\r\n\x05index\x18\x02 \x01(\r\x12\r\n\x05\x64\x65\x62ug\x18\x03 \x01(\x08\x12\x0c\n\x04\x63ost\x18\x04 \x01(\x02\x12\x0e\n\x06labels\x18\x1e \x03(\t\x12\x19\n\x0finput_object_id\x18\n \x01(\tH\x00\x12\x17\n\rinput_content\x18\x0b \x01(\tH\x00\x12\x13\n\tinput_url\x18\x0c \x01(\tH\x00\x12\x44\n\x0finput_generator\x18\r \x01(\x0b\x32).eolymp.executor.EvaluationTask.GeneratorH\x00\x12\x1a\n\x10\x61nswer_object_id\x18\x14 \x01(\tH\x01\x12\x18\n\x0e\x61nswer_content\x18\x15 \x01(\tH\x01\x12\x14\n\nanswer_url\x18\x16 \x01(\tH\x01\x12\x45\n\x10\x61nswer_generator\x18\x17 \x01(\x0b\x32).eolymp.executor.EvaluationTask.GeneratorH\x01\x42\x07\n\x05inputB\x08\n\x06\x61nswer\x1ai\n\x0cPrecondition\x12\x10\n\x08selector\x18\x01 \x03(\t\x12\x12\n\ndepends_on\x18\n \x03(\t\x12\x17\n\x0fstop_on_failure\x18\x0b \x01(\x08\x12\x1a\n\x12max_execution_time\x18\x0c \x01(\r\x1a\x8d\x01\n\nConstraint\x12\x10\n\x08selector\x18\x01 \x03(\t\x12\r\n\x05\x61\x63tor\x18\x02 \x01(\t\x12\x17\n\x0fwall_time_limit\x18\n \x01(\r\x12\x16\n\x0e\x63pu_time_limit\x18\x0b \x01(\r\x12\x14\n\x0cmemory_limit\x18\x0c \x01(\x04\x12\x17\n\x0f\x66ile_size_limit\x18\r \x01(\x04\x42\x33Z1github.com/eolymp/go-sdk/eolymp/executor;executorb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.executor.evaluation_task_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/executor;executor'
  _EVALUATIONTASK._serialized_start=182
  _EVALUATIONTASK._serialized_end=1472
  _EVALUATIONTASK_GENERATOR._serialized_start=774
  _EVALUATIONTASK_GENERATOR._serialized_end=825
  _EVALUATIONTASK_RUN._serialized_start=828
  _EVALUATIONTASK_RUN._serialized_end=1221
  _EVALUATIONTASK_PRECONDITION._serialized_start=1223
  _EVALUATIONTASK_PRECONDITION._serialized_end=1328
  _EVALUATIONTASK_CONSTRAINT._serialized_start=1331
  _EVALUATIONTASK_CONSTRAINT._serialized_end=1472
# @@protoc_insertion_point(module_scope)
