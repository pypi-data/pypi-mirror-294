# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/universe/plan.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.ecm import content_pb2 as eolymp_dot_ecm_dot_content__pb2
from eolymp.universe import quota_pb2 as eolymp_dot_universe_dot_quota__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1a\x65olymp/universe/plan.proto\x12\x0f\x65olymp.universe\x1a\x18\x65olymp/ecm/content.proto\x1a\x1b\x65olymp/universe/quota.proto\"\xde\x03\n\x04Plan\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12(\n\x0b\x64\x65scription\x18\x03 \x01(\x0b\x32\x13.eolymp.ecm.Content\x12%\n\x05quota\x18\x04 \x01(\x0b\x32\x16.eolymp.universe.Quota\x12\x0e\n\x06labels\x18\x05 \x03(\t\x12\x11\n\tmin_seats\x18\n \x01(\r\x12\x11\n\tmax_seats\x18\x0b \x01(\r\x12/\n\x08variants\x18\x64 \x03(\x0b\x32\x1d.eolymp.universe.Plan.Variant\x1ar\n\x07Variant\x12\n\n\x02id\x18\x01 \x01(\t\x12\x34\n\nrecurrence\x18\x03 \x01(\x0e\x32 .eolymp.universe.Plan.Recurrence\x12\x10\n\x08\x63urrency\x18\x1e \x01(\t\x12\x13\n\x0bunit_amount\x18\x1f \x01(\x05\"D\n\x05\x45xtra\x12\x0c\n\x08NO_EXTRA\x10\x00\x12\x16\n\x12\x44\x45SCRIPTION_RENDER\x10\x01\x12\x15\n\x11\x44\x45SCRIPTION_VALUE\x10\x02\"J\n\nRecurrence\x12\x16\n\x12UNKNOWN_RECURRENCE\x10\x00\x12\x0b\n\x07ONETIME\x10\x01\x12\x0b\n\x07MONTHLY\x10\x02\x12\n\n\x06YEARLY\x10\x03\x42\x33Z1github.com/eolymp/go-sdk/eolymp/universe;universeb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.universe.plan_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/universe;universe'
  _PLAN._serialized_start=103
  _PLAN._serialized_end=581
  _PLAN_VARIANT._serialized_start=321
  _PLAN_VARIANT._serialized_end=435
  _PLAN_EXTRA._serialized_start=437
  _PLAN_EXTRA._serialized_end=505
  _PLAN_RECURRENCE._serialized_start=507
  _PLAN_RECURRENCE._serialized_end=581
# @@protoc_insertion_point(module_scope)
