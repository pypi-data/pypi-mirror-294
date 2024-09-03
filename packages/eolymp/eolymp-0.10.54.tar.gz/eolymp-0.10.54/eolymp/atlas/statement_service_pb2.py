# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/atlas/statement_service.proto
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
from eolymp.atlas import statement_pb2 as eolymp_dot_atlas_dot_statement__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$eolymp/atlas/statement_service.proto\x12\x0c\x65olymp.atlas\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1e\x65olymp/annotations/scope.proto\x1a\x1c\x65olymp/atlas/statement.proto\"J\n\x13ListStatementsInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x0e\n\x06render\x18\x02 \x01(\x08\x12\x0f\n\x07version\x18\x64 \x01(\r\"M\n\x14ListStatementsOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12&\n\x05items\x18\x02 \x03(\x0b\x32\x17.eolymp.atlas.Statement\"c\n\x16\x44\x65scribeStatementInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x14\n\x0cstatement_id\x18\x02 \x01(\t\x12\x0e\n\x06render\x18\x03 \x01(\x08\x12\x0f\n\x07version\x18\x64 \x01(\r\"E\n\x17\x44\x65scribeStatementOutput\x12*\n\tstatement\x18\x01 \x01(\x0b\x32\x17.eolymp.atlas.Statement\"[\n\x14LookupStatementInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x0e\n\x06locale\x18\x02 \x01(\t\x12\x0e\n\x06render\x18\x03 \x01(\x08\x12\x0f\n\x07version\x18\x64 \x01(\r\"C\n\x15LookupStatementOutput\x12*\n\tstatement\x18\x01 \x01(\x0b\x32\x17.eolymp.atlas.Statement\"W\n\x15PreviewStatementInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12*\n\tstatement\x18\x02 \x01(\x0b\x32\x17.eolymp.atlas.Statement\"D\n\x16PreviewStatementOutput\x12*\n\tstatement\x18\x01 \x01(\x0b\x32\x17.eolymp.atlas.Statement\"V\n\x14\x43reateStatementInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12*\n\tstatement\x18\x02 \x01(\x0b\x32\x17.eolymp.atlas.Statement\"-\n\x15\x43reateStatementOutput\x12\x14\n\x0cstatement_id\x18\x01 \x01(\t\"\x86\x02\n\x14UpdateStatementInput\x12\x37\n\x05patch\x18\n \x03(\x0e\x32(.eolymp.atlas.UpdateStatementInput.Patch\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x14\n\x0cstatement_id\x18\x02 \x01(\t\x12*\n\tstatement\x18\x03 \x01(\x0b\x32\x17.eolymp.atlas.Statement\"_\n\x05Patch\x12\x07\n\x03\x41LL\x10\x00\x12\n\n\x06LOCALE\x10\x01\x12\t\n\x05TITLE\x10\x02\x12\x0b\n\x07\x43ONTENT\x10\x03\x12\x11\n\rDOWNLOAD_LINK\x10\x04\x12\n\n\x06\x41UTHOR\x10\x05\x12\n\n\x06SOURCE\x10\x06\"\x17\n\x15UpdateStatementOutput\"@\n\x14\x44\x65leteStatementInput\x12\x12\n\nproblem_id\x18\x01 \x01(\t\x12\x14\n\x0cstatement_id\x18\x02 \x01(\t\"\x17\n\x15\x44\x65leteStatementOutput2\x81\t\n\x10StatementService\x12\x99\x01\n\x0f\x43reateStatement\x12\".eolymp.atlas.CreateStatementInput\x1a#.eolymp.atlas.CreateStatementOutput\"=\x82\xe3\n\x17\x8a\xe3\n\x13\x61tlas:problem:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\r\x1a\x0b/statements\x12\xa8\x01\n\x0fUpdateStatement\x12\".eolymp.atlas.UpdateStatementInput\x1a#.eolymp.atlas.UpdateStatementOutput\"L\x82\xe3\n\x17\x8a\xe3\n\x13\x61tlas:problem:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\x1c\x1a\x1a/statements/{statement_id}\x12\xa8\x01\n\x0f\x44\x65leteStatement\x12\".eolymp.atlas.DeleteStatementInput\x1a#.eolymp.atlas.DeleteStatementOutput\"L\x82\xe3\n\x17\x8a\xe3\n\x13\x61tlas:problem:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\x1c*\x1a/statements/{statement_id}\x12\xad\x01\n\x11\x44\x65scribeStatement\x12$.eolymp.atlas.DescribeStatementInput\x1a%.eolymp.atlas.DescribeStatementOutput\"K\x82\xe3\n\x16\x8a\xe3\n\x12\x61tlas:problem:read\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\nd\x82\xd3\xe4\x93\x02\x1c\x12\x1a/statements/{statement_id}\x12\x97\x01\n\x0fLookupStatement\x12\".eolymp.atlas.LookupStatementInput\x1a#.eolymp.atlas.LookupStatementOutput\";\x82\xe3\n\x16\x8a\xe3\n\x12\x61tlas:problem:read\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\nd\x82\xd3\xe4\x93\x02\x0c\x12\n/translate\x12\x98\x01\n\x10PreviewStatement\x12#.eolymp.atlas.PreviewStatementInput\x1a$.eolymp.atlas.PreviewStatementOutput\"9\x82\xe3\n\x16\x8a\xe3\n\x12\x61tlas:problem:read\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\nd\x82\xd3\xe4\x93\x02\n\"\x08/renders\x12\x95\x01\n\x0eListStatements\x12!.eolymp.atlas.ListStatementsInput\x1a\".eolymp.atlas.ListStatementsOutput\"<\x82\xe3\n\x16\x8a\xe3\n\x12\x61tlas:problem:read\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\nd\x82\xd3\xe4\x93\x02\r\x12\x0b/statementsB-Z+github.com/eolymp/go-sdk/eolymp/atlas;atlasb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.atlas.statement_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z+github.com/eolymp/go-sdk/eolymp/atlas;atlas'
  _STATEMENTSERVICE.methods_by_name['CreateStatement']._options = None
  _STATEMENTSERVICE.methods_by_name['CreateStatement']._serialized_options = b'\202\343\n\027\212\343\n\023atlas:problem:write\352\342\n\013\365\342\n\000\000\200?\370\342\n\005\202\323\344\223\002\r\032\013/statements'
  _STATEMENTSERVICE.methods_by_name['UpdateStatement']._options = None
  _STATEMENTSERVICE.methods_by_name['UpdateStatement']._serialized_options = b'\202\343\n\027\212\343\n\023atlas:problem:write\352\342\n\013\365\342\n\000\000\200?\370\342\n\005\202\323\344\223\002\034\032\032/statements/{statement_id}'
  _STATEMENTSERVICE.methods_by_name['DeleteStatement']._options = None
  _STATEMENTSERVICE.methods_by_name['DeleteStatement']._serialized_options = b'\202\343\n\027\212\343\n\023atlas:problem:write\352\342\n\013\365\342\n\000\000\200?\370\342\n\005\202\323\344\223\002\034*\032/statements/{statement_id}'
  _STATEMENTSERVICE.methods_by_name['DescribeStatement']._options = None
  _STATEMENTSERVICE.methods_by_name['DescribeStatement']._serialized_options = b'\202\343\n\026\212\343\n\022atlas:problem:read\352\342\n\013\365\342\n\000\000\240A\370\342\nd\202\323\344\223\002\034\022\032/statements/{statement_id}'
  _STATEMENTSERVICE.methods_by_name['LookupStatement']._options = None
  _STATEMENTSERVICE.methods_by_name['LookupStatement']._serialized_options = b'\202\343\n\026\212\343\n\022atlas:problem:read\352\342\n\013\365\342\n\000\000\240A\370\342\nd\202\323\344\223\002\014\022\n/translate'
  _STATEMENTSERVICE.methods_by_name['PreviewStatement']._options = None
  _STATEMENTSERVICE.methods_by_name['PreviewStatement']._serialized_options = b'\202\343\n\026\212\343\n\022atlas:problem:read\352\342\n\013\365\342\n\000\000\240A\370\342\nd\202\323\344\223\002\n\"\010/renders'
  _STATEMENTSERVICE.methods_by_name['ListStatements']._options = None
  _STATEMENTSERVICE.methods_by_name['ListStatements']._serialized_options = b'\202\343\n\026\212\343\n\022atlas:problem:read\352\342\n\013\365\342\n\000\000\240A\370\342\nd\202\323\344\223\002\r\022\013/statements'
  _LISTSTATEMENTSINPUT._serialized_start=183
  _LISTSTATEMENTSINPUT._serialized_end=257
  _LISTSTATEMENTSOUTPUT._serialized_start=259
  _LISTSTATEMENTSOUTPUT._serialized_end=336
  _DESCRIBESTATEMENTINPUT._serialized_start=338
  _DESCRIBESTATEMENTINPUT._serialized_end=437
  _DESCRIBESTATEMENTOUTPUT._serialized_start=439
  _DESCRIBESTATEMENTOUTPUT._serialized_end=508
  _LOOKUPSTATEMENTINPUT._serialized_start=510
  _LOOKUPSTATEMENTINPUT._serialized_end=601
  _LOOKUPSTATEMENTOUTPUT._serialized_start=603
  _LOOKUPSTATEMENTOUTPUT._serialized_end=670
  _PREVIEWSTATEMENTINPUT._serialized_start=672
  _PREVIEWSTATEMENTINPUT._serialized_end=759
  _PREVIEWSTATEMENTOUTPUT._serialized_start=761
  _PREVIEWSTATEMENTOUTPUT._serialized_end=829
  _CREATESTATEMENTINPUT._serialized_start=831
  _CREATESTATEMENTINPUT._serialized_end=917
  _CREATESTATEMENTOUTPUT._serialized_start=919
  _CREATESTATEMENTOUTPUT._serialized_end=964
  _UPDATESTATEMENTINPUT._serialized_start=967
  _UPDATESTATEMENTINPUT._serialized_end=1229
  _UPDATESTATEMENTINPUT_PATCH._serialized_start=1134
  _UPDATESTATEMENTINPUT_PATCH._serialized_end=1229
  _UPDATESTATEMENTOUTPUT._serialized_start=1231
  _UPDATESTATEMENTOUTPUT._serialized_end=1254
  _DELETESTATEMENTINPUT._serialized_start=1256
  _DELETESTATEMENTINPUT._serialized_end=1320
  _DELETESTATEMENTOUTPUT._serialized_start=1322
  _DELETESTATEMENTOUTPUT._serialized_end=1345
  _STATEMENTSERVICE._serialized_start=1348
  _STATEMENTSERVICE._serialized_end=2501
# @@protoc_insertion_point(module_scope)
