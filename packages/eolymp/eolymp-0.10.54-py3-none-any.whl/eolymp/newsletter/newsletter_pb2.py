# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/newsletter/newsletter.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.ecm import content_pb2 as eolymp_dot_ecm_dot_content__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"eolymp/newsletter/newsletter.proto\x12\x11\x65olymp.newsletter\x1a\x18\x65olymp/ecm/content.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xe1\x01\n\nNewsletter\x12\n\n\x02id\x18\x01 \x01(\t\x12.\n\ncreated_at\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x07subject\x18\x0b \x01(\t\x12$\n\x07\x63ontent\x18\x0c \x01(\x0b\x32\x13.eolymp.ecm.Content\x1a`\n\x0bTranslation\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06locale\x18\x66 \x01(\t\x12\x0f\n\x07subject\x18g \x01(\t\x12$\n\x07\x63ontent\x18h \x01(\x0b\x32\x13.eolymp.ecm.ContentB7Z5github.com/eolymp/go-sdk/eolymp/newsletter;newsletterb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.newsletter.newsletter_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z5github.com/eolymp/go-sdk/eolymp/newsletter;newsletter'
  _NEWSLETTER._serialized_start=117
  _NEWSLETTER._serialized_end=342
  _NEWSLETTER_TRANSLATION._serialized_start=246
  _NEWSLETTER_TRANSLATION._serialized_end=342
# @@protoc_insertion_point(module_scope)
