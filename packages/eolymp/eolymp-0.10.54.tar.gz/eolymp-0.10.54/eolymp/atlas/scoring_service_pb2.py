# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/atlas/scoring_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import http_pb2 as eolymp_dot_annotations_dot_http__pb2
from eolymp.annotations import scope_pb2 as eolymp_dot_annotations_dot_scope__pb2
from eolymp.atlas import scoring_score_pb2 as eolymp_dot_atlas_dot_scoring__score__pb2
from eolymp.atlas import submission_pb2 as eolymp_dot_atlas_dot_submission__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"eolymp/atlas/scoring_service.proto\x12\x0c\x65olymp.atlas\x1a\x1d\x65olymp/annotations/http.proto\x1a\x1e\x65olymp/annotations/scope.proto\x1a eolymp/atlas/scoring_score.proto\x1a\x1d\x65olymp/atlas/submission.proto\";\n\x12\x44\x65scribeScoreInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x11\n\tmember_id\x18\x02 \x01(\t\"9\n\x13\x44\x65scribeScoreOutput\x12\"\n\x05score\x18\x01 \x01(\x0b\x32\x13.eolymp.atlas.Score\")\n\x13ListProblemTopInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\"?\n\x14ListProblemTopOutput\x12\'\n\x05items\x18\x02 \x03(\x0b\x32\x18.eolymp.atlas.Submission\"1\n\x1b\x44\x65scribeProblemGradingInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\"\x8d\x01\n\x1c\x44\x65scribeProblemGradingOutput\x12@\n\x06ranges\x18\x02 \x03(\x0b\x32\x30.eolymp.atlas.DescribeProblemGradingOutput.Range\x1a+\n\x05Range\x12\r\n\x05grade\x18\x01 \x01(\r\x12\x13\n\x0bupper_bound\x18\x02 \x01(\x02\x32\xc0\x03\n\x0eScoringService\x12\x8e\x01\n\rDescribeScore\x12 .eolymp.atlas.DescribeScoreInput\x1a!.eolymp.atlas.DescribeScoreOutput\"8\x82\xe3\n\x19\x8a\xe3\n\x15\x61tlas:submission:read\x82\xd3\xe4\x93\x02\x15\x12\x13/scores/{member_id}\x12\x9b\x01\n\x16\x44\x65scribeProblemGrading\x12).eolymp.atlas.DescribeProblemGradingInput\x1a*.eolymp.atlas.DescribeProblemGradingOutput\"*\x82\xe3\n\x16\x8a\xe3\n\x12\x61tlas:problem:read\x82\xd3\xe4\x93\x02\n\x12\x08/grading\x12\x7f\n\x0eListProblemTop\x12!.eolymp.atlas.ListProblemTopInput\x1a\".eolymp.atlas.ListProblemTopOutput\"&\x82\xe3\n\x16\x8a\xe3\n\x12\x61tlas:problem:read\x82\xd3\xe4\x93\x02\x06\x12\x04/topB-Z+github.com/eolymp/go-sdk/eolymp/atlas;atlasb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.atlas.scoring_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z+github.com/eolymp/go-sdk/eolymp/atlas;atlas'
  _SCORINGSERVICE.methods_by_name['DescribeScore']._options = None
  _SCORINGSERVICE.methods_by_name['DescribeScore']._serialized_options = b'\202\343\n\031\212\343\n\025atlas:submission:read\202\323\344\223\002\025\022\023/scores/{member_id}'
  _SCORINGSERVICE.methods_by_name['DescribeProblemGrading']._options = None
  _SCORINGSERVICE.methods_by_name['DescribeProblemGrading']._serialized_options = b'\202\343\n\026\212\343\n\022atlas:problem:read\202\323\344\223\002\n\022\010/grading'
  _SCORINGSERVICE.methods_by_name['ListProblemTop']._options = None
  _SCORINGSERVICE.methods_by_name['ListProblemTop']._serialized_options = b'\202\343\n\026\212\343\n\022atlas:problem:read\202\323\344\223\002\006\022\004/top'
  _DESCRIBESCOREINPUT._serialized_start=180
  _DESCRIBESCOREINPUT._serialized_end=239
  _DESCRIBESCOREOUTPUT._serialized_start=241
  _DESCRIBESCOREOUTPUT._serialized_end=298
  _LISTPROBLEMTOPINPUT._serialized_start=300
  _LISTPROBLEMTOPINPUT._serialized_end=341
  _LISTPROBLEMTOPOUTPUT._serialized_start=343
  _LISTPROBLEMTOPOUTPUT._serialized_end=406
  _DESCRIBEPROBLEMGRADINGINPUT._serialized_start=408
  _DESCRIBEPROBLEMGRADINGINPUT._serialized_end=457
  _DESCRIBEPROBLEMGRADINGOUTPUT._serialized_start=460
  _DESCRIBEPROBLEMGRADINGOUTPUT._serialized_end=601
  _DESCRIBEPROBLEMGRADINGOUTPUT_RANGE._serialized_start=558
  _DESCRIBEPROBLEMGRADINGOUTPUT_RANGE._serialized_end=601
  _SCORINGSERVICE._serialized_start=604
  _SCORINGSERVICE._serialized_end=1052
# @@protoc_insertion_point(module_scope)
