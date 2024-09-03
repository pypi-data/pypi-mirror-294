# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/atlas/submission_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import http_pb2 as eolymp_dot_annotations_dot_http__pb2
from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2
from eolymp.annotations import scope_pb2 as eolymp_dot_annotations_dot_scope__pb2
from eolymp.atlas import submission_pb2 as eolymp_dot_atlas_dot_submission__pb2
from eolymp.wellknown import expression_pb2 as eolymp_dot_wellknown_dot_expression__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%eolymp/atlas/submission_service.proto\x12\x0c\x65olymp.atlas\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1e\x65olymp/annotations/scope.proto\x1a\x1d\x65olymp/atlas/submission.proto\x1a!eolymp/wellknown/expression.proto\"I\n\x15\x43reateSubmissionInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x0c\n\x04lang\x18\x02 \x01(\t\x12\x0e\n\x06source\x18\x03 \x01(\t\"/\n\x16\x43reateSubmissionOutput\x12\x15\n\rsubmission_id\x18\x01 \x01(\t\"D\n\x17\x44\x65scribeSubmissionInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x15\n\rsubmission_id\x18\x02 \x01(\t\"x\n\x18\x44\x65scribeSubmissionOutput\x12,\n\nsubmission\x18\x01 \x01(\x0b\x32\x18.eolymp.atlas.Submission\x12.\n\x05\x65xtra\x18\xe3\x08 \x03(\x0e\x32\x1e.eolymp.atlas.Submission.Extra\"q\n\x14WatchSubmissionInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x15\n\rsubmission_id\x18\x02 \x01(\t\x12.\n\x05\x65xtra\x18\xe3\x08 \x03(\x0e\x32\x1e.eolymp.atlas.Submission.Extra\"E\n\x15WatchSubmissionOutput\x12,\n\nsubmission\x18\x01 \x01(\x0b\x32\x18.eolymp.atlas.Submission\"Q\n\x15RetestSubmissionInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x15\n\rsubmission_id\x18\x02 \x01(\t\x12\r\n\x05\x64\x65\x62ug\x18\x03 \x01(\x08\"\x18\n\x16RetestSubmissionOutput\"\x9d\x05\n\x14ListSubmissionsInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\r\n\x05\x61\x66ter\x18\x0c \x01(\t\x12\x0e\n\x06offset\x18\n \x01(\x05\x12\x0c\n\x04size\x18\x0b \x01(\x05\x12:\n\x07\x66ilters\x18( \x01(\x0b\x32).eolymp.atlas.ListSubmissionsInput.Filter\x12.\n\x05\x65xtra\x18\xe3\x08 \x03(\x0e\x32\x1e.eolymp.atlas.Submission.Extra\x1a\xd7\x03\n\x06\x46ilter\x12*\n\x02id\x18\x01 \x03(\x0b\x32\x1e.eolymp.wellknown.ExpressionID\x12\x32\n\nproblem_id\x18\x02 \x03(\x0b\x32\x1e.eolymp.wellknown.ExpressionID\x12/\n\x07user_id\x18\x03 \x03(\x0b\x32\x1e.eolymp.wellknown.ExpressionID\x12\x31\n\tmember_id\x18\t \x03(\x0b\x32\x1e.eolymp.wellknown.ExpressionID\x12;\n\x0csubmitted_at\x18\x04 \x03(\x0b\x32%.eolymp.wellknown.ExpressionTimestamp\x12\x31\n\x07runtime\x18\x05 \x03(\x0b\x32 .eolymp.wellknown.ExpressionEnum\x12\x30\n\x06status\x18\x06 \x03(\x0b\x32 .eolymp.wellknown.ExpressionEnum\x12\x30\n\x05score\x18\x07 \x03(\x0b\x32!.eolymp.wellknown.ExpressionFloat\x12\x35\n\npercentage\x18\x08 \x03(\x0b\x32!.eolymp.wellknown.ExpressionFloat\"\x83\x01\n\x15ListSubmissionsOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12\'\n\x05items\x18\x02 \x03(\x0b\x32\x18.eolymp.atlas.Submission\x12\x18\n\x10next_page_cursor\x18\x03 \x01(\t\x12\x18\n\x10prev_page_cursor\x18\x04 \x01(\t2\xc4\x06\n\x11SubmissionService\x12\xa0\x01\n\x10\x43reateSubmission\x12#.eolymp.atlas.CreateSubmissionInput\x1a$.eolymp.atlas.CreateSubmissionOutput\"A\xea\xe2\n\x0b\xf5\xe2\n\n\xd7#>\xf8\xe2\n\x05\x82\xe3\n\x1a\x8a\xe3\n\x16\x61tlas:submission:write\x82\xd3\xe4\x93\x02\x0e\"\x0c/submissions\x12\xb7\x01\n\x10RetestSubmission\x12#.eolymp.atlas.RetestSubmissionInput\x1a$.eolymp.atlas.RetestSubmissionOutput\"X\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\n\x82\xe3\n\x1a\x8a\xe3\n\x16\x61tlas:submission:write\x82\xd3\xe4\x93\x02%\"#/submissions/{submission_id}/retest\x12\xb5\x01\n\x12\x44\x65scribeSubmission\x12%.eolymp.atlas.DescribeSubmissionInput\x1a&.eolymp.atlas.DescribeSubmissionOutput\"P\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n\n\x82\xe3\n\x19\x8a\xe3\n\x15\x61tlas:submission:read\x82\xd3\xe4\x93\x02\x1e\x12\x1c/submissions/{submission_id}\x12{\n\x0fWatchSubmission\x12\".eolymp.atlas.WatchSubmissionInput\x1a#.eolymp.atlas.WatchSubmissionOutput\"\x1d\x82\xe3\n\x19\x8a\xe3\n\x15\x61tlas:submission:read0\x01\x12\x9c\x01\n\x0fListSubmissions\x12\".eolymp.atlas.ListSubmissionsInput\x1a#.eolymp.atlas.ListSubmissionsOutput\"@\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n\n\x82\xe3\n\x19\x8a\xe3\n\x15\x61tlas:submission:read\x82\xd3\xe4\x93\x02\x0e\x12\x0c/submissionsB-Z+github.com/eolymp/go-sdk/eolymp/atlas;atlasb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.atlas.submission_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z+github.com/eolymp/go-sdk/eolymp/atlas;atlas'
  _SUBMISSIONSERVICE.methods_by_name['CreateSubmission']._options = None
  _SUBMISSIONSERVICE.methods_by_name['CreateSubmission']._serialized_options = b'\352\342\n\013\365\342\n\n\327#>\370\342\n\005\202\343\n\032\212\343\n\026atlas:submission:write\202\323\344\223\002\016\"\014/submissions'
  _SUBMISSIONSERVICE.methods_by_name['RetestSubmission']._options = None
  _SUBMISSIONSERVICE.methods_by_name['RetestSubmission']._serialized_options = b'\352\342\n\013\365\342\n\000\000\200?\370\342\n\n\202\343\n\032\212\343\n\026atlas:submission:write\202\323\344\223\002%\"#/submissions/{submission_id}/retest'
  _SUBMISSIONSERVICE.methods_by_name['DescribeSubmission']._options = None
  _SUBMISSIONSERVICE.methods_by_name['DescribeSubmission']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240@\370\342\n\n\202\343\n\031\212\343\n\025atlas:submission:read\202\323\344\223\002\036\022\034/submissions/{submission_id}'
  _SUBMISSIONSERVICE.methods_by_name['WatchSubmission']._options = None
  _SUBMISSIONSERVICE.methods_by_name['WatchSubmission']._serialized_options = b'\202\343\n\031\212\343\n\025atlas:submission:read'
  _SUBMISSIONSERVICE.methods_by_name['ListSubmissions']._options = None
  _SUBMISSIONSERVICE.methods_by_name['ListSubmissions']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240@\370\342\n\n\202\343\n\031\212\343\n\025atlas:submission:read\202\323\344\223\002\016\022\014/submissions'
  _CREATESUBMISSIONINPUT._serialized_start=220
  _CREATESUBMISSIONINPUT._serialized_end=293
  _CREATESUBMISSIONOUTPUT._serialized_start=295
  _CREATESUBMISSIONOUTPUT._serialized_end=342
  _DESCRIBESUBMISSIONINPUT._serialized_start=344
  _DESCRIBESUBMISSIONINPUT._serialized_end=412
  _DESCRIBESUBMISSIONOUTPUT._serialized_start=414
  _DESCRIBESUBMISSIONOUTPUT._serialized_end=534
  _WATCHSUBMISSIONINPUT._serialized_start=536
  _WATCHSUBMISSIONINPUT._serialized_end=649
  _WATCHSUBMISSIONOUTPUT._serialized_start=651
  _WATCHSUBMISSIONOUTPUT._serialized_end=720
  _RETESTSUBMISSIONINPUT._serialized_start=722
  _RETESTSUBMISSIONINPUT._serialized_end=803
  _RETESTSUBMISSIONOUTPUT._serialized_start=805
  _RETESTSUBMISSIONOUTPUT._serialized_end=829
  _LISTSUBMISSIONSINPUT._serialized_start=832
  _LISTSUBMISSIONSINPUT._serialized_end=1501
  _LISTSUBMISSIONSINPUT_FILTER._serialized_start=1030
  _LISTSUBMISSIONSINPUT_FILTER._serialized_end=1501
  _LISTSUBMISSIONSOUTPUT._serialized_start=1504
  _LISTSUBMISSIONSOUTPUT._serialized_end=1635
  _SUBMISSIONSERVICE._serialized_start=1638
  _SUBMISSIONSERVICE._serialized_end=2474
# @@protoc_insertion_point(module_scope)
