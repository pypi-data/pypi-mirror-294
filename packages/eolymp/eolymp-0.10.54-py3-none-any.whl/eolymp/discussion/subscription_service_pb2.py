# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/discussion/subscription_service.proto
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
from eolymp.discussion import subscription_pb2 as eolymp_dot_discussion_dot_subscription__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n,eolymp/discussion/subscription_service.proto\x12\x11\x65olymp.discussion\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1e\x65olymp/annotations/scope.proto\x1a$eolymp/discussion/subscription.proto\"\x1b\n\x19\x44\x65scribeSubscriptionInput\"S\n\x1a\x44\x65scribeSubscriptionOutput\x12\x35\n\x0csubscription\x18\x01 \x01(\x0b\x32\x1f.eolymp.discussion.Subscription\"P\n\x17UpdateSubscriptionInput\x12\x35\n\x0csubscription\x18\x01 \x01(\x0b\x32\x1f.eolymp.discussion.Subscription\"\x1a\n\x18UpdateSubscriptionOutput2\x91\x03\n\x13SubscriptionService\x12\xbe\x01\n\x14\x44\x65scribeSubscription\x12,.eolymp.discussion.DescribeSubscriptionInput\x1a-.eolymp.discussion.DescribeSubscriptionOutput\"I\x82\xe3\n \x8a\xe3\n\x1c\x64iscussion:subscription:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02\x0f\x12\r/subscription\x12\xb8\x01\n\x12UpdateSubscription\x12*.eolymp.discussion.UpdateSubscriptionInput\x1a+.eolymp.discussion.UpdateSubscriptionOutput\"I\x82\xe3\n!\x8a\xe3\n\x1d\x64iscussion:subscription:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\x0f\x1a\r/subscriptionB7Z5github.com/eolymp/go-sdk/eolymp/discussion;discussionb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.discussion.subscription_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z5github.com/eolymp/go-sdk/eolymp/discussion;discussion'
  _SUBSCRIPTIONSERVICE.methods_by_name['DescribeSubscription']._options = None
  _SUBSCRIPTIONSERVICE.methods_by_name['DescribeSubscription']._serialized_options = b'\202\343\n \212\343\n\034discussion:subscription:read\352\342\n\014\365\342\n\000\000\240A\370\342\n\364\003\202\323\344\223\002\017\022\r/subscription'
  _SUBSCRIPTIONSERVICE.methods_by_name['UpdateSubscription']._options = None
  _SUBSCRIPTIONSERVICE.methods_by_name['UpdateSubscription']._serialized_options = b'\202\343\n!\212\343\n\035discussion:subscription:write\352\342\n\013\365\342\n\000\000\200?\370\342\n\005\202\323\344\223\002\017\032\r/subscription'
  _DESCRIBESUBSCRIPTIONINPUT._serialized_start=204
  _DESCRIBESUBSCRIPTIONINPUT._serialized_end=231
  _DESCRIBESUBSCRIPTIONOUTPUT._serialized_start=233
  _DESCRIBESUBSCRIPTIONOUTPUT._serialized_end=316
  _UPDATESUBSCRIPTIONINPUT._serialized_start=318
  _UPDATESUBSCRIPTIONINPUT._serialized_end=398
  _UPDATESUBSCRIPTIONOUTPUT._serialized_start=400
  _UPDATESUBSCRIPTIONOUTPUT._serialized_end=426
  _SUBSCRIPTIONSERVICE._serialized_start=429
  _SUBSCRIPTIONSERVICE._serialized_end=830
# @@protoc_insertion_point(module_scope)
