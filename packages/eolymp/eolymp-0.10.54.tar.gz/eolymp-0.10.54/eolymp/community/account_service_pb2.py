# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/community/account_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.annotations import http_pb2 as eolymp_dot_annotations_dot_http__pb2
from eolymp.annotations import ratelimit_pb2 as eolymp_dot_annotations_dot_ratelimit__pb2
from eolymp.community import member_pb2 as eolymp_dot_community_dot_member__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&eolymp/community/account_service.proto\x12\x10\x65olymp.community\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1d\x65olymp/community/member.proto\"O\n\x12\x43reateAccountInput\x12(\n\x06member\x18\x01 \x01(\x0b\x32\x18.eolymp.community.Member\x12\x0f\n\x07\x63\x61ptcha\x18\x64 \x01(\t\"6\n\x13\x43reateAccountOutput\x12\x11\n\tmember_id\x18\x01 \x01(\t\x12\x0c\n\x04hint\x18\x64 \x01(\t\"\x16\n\x14\x44\x65scribeAccountInput\"\x99\x01\n\x15\x44\x65scribeAccountOutput\x12(\n\x06member\x18\x01 \x01(\x0b\x32\x18.eolymp.community.Member\x12&\n\x04team\x18\x02 \x01(\x0b\x32\x18.eolymp.community.Member\x12.\n\x05\x65xtra\x18\xe3\x08 \x03(\x0e\x32\x1e.eolymp.community.Member.Extra\"\xd3\x03\n\x12UpdateAccountInput\x12\x39\n\x05patch\x18\x01 \x03(\x0e\x32*.eolymp.community.UpdateAccountInput.Patch\x12\x18\n\x10\x63urrent_password\x18\x02 \x01(\t\x12(\n\x06member\x18\n \x01(\x0b\x32\x18.eolymp.community.Member\"\xbd\x02\n\x05Patch\x12\x07\n\x03\x41LL\x10\x00\x12\x11\n\rUSER_NICKNAME\x10\x65\x12\x0e\n\nUSER_EMAIL\x10\x66\x12\x11\n\rUSER_PASSWORD\x10g\x12\r\n\tUSER_NAME\x10h\x12\x10\n\x0cUSER_PICTURE\x10i\x12\x11\n\rUSER_BIRTHDAY\x10j\x12\x10\n\x0cUSER_COUNTRY\x10k\x12\r\n\tUSER_CITY\x10l\x12\x14\n\x10USER_PREFERENCES\x10m\x12\x1c\n\x17USER_PREFERENCES_LOCALE\x10\xbe\x01\x12\x1e\n\x19USER_PREFERENCES_TIMEZONE\x10\xbf\x01\x12\x1d\n\x18USER_PREFERENCES_RUNTIME\x10\xc0\x01\x12\x1c\n\x18USER_EMAIL_SUBSCRIPTIONS\x10n\x12\x0f\n\nATTRIBUTES\x10\x84\x07\"#\n\x13UpdateAccountOutput\x12\x0c\n\x04hint\x18\x01 \x01(\t\"f\n\x12UploadPictureInput\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12\x10\n\x08offset_x\x18\n \x01(\r\x12\x10\n\x08offset_y\x18\x0b \x01(\r\x12\x0c\n\x04size\x18\x0c \x01(\r\"*\n\x13UploadPictureOutput\x12\x13\n\x0bpicture_url\x18\x01 \x01(\t\"\x14\n\x12\x44\x65leteAccountInput\"\x15\n\x13\x44\x65leteAccountOutput\"\x19\n\x17ResendVerificationInput\"\x1a\n\x18ResendVerificationOutput\"<\n\x19\x43ompleteVerificationInput\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x11\n\tmember_id\x18\x02 \x01(\t\"\x1c\n\x1a\x43ompleteVerificationOutput\"D\n\x12StartRecoveryInput\x12\r\n\x05\x65mail\x18\x01 \x01(\t\x12\x0e\n\x06locale\x18\x02 \x01(\t\x12\x0f\n\x07\x63\x61ptcha\x18\x64 \x01(\t\"6\n\x13StartRecoveryOutput\x12\x0c\n\x04hint\x18\x01 \x01(\t\x12\x11\n\tmember_id\x18\x02 \x01(\t\"I\n\x14\x43ompleteRecoverInput\x12\x0c\n\x04\x63ode\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x11\n\tmember_id\x18\x03 \x01(\t\"\x17\n\x15\x43ompleteRecoverOutput2\x91\n\n\x0e\x41\x63\x63ountService\x12}\n\rCreateAccount\x12$.eolymp.community.CreateAccountInput\x1a%.eolymp.community.CreateAccountOutput\"\x1f\xea\xe2\n\x0b\xf5\xe2\n\x00\x00 A\xf8\xe2\n2\x82\xd3\xe4\x93\x02\n\"\x08/account\x12\x83\x01\n\x0f\x44\x65scribeAccount\x12&.eolymp.community.DescribeAccountInput\x1a\'.eolymp.community.DescribeAccountOutput\"\x1f\xea\xe2\n\x0b\xf5\xe2\n\x00\x00 A\xf8\xe2\n2\x82\xd3\xe4\x93\x02\n\x12\x08/account\x12}\n\rUpdateAccount\x12$.eolymp.community.UpdateAccountInput\x1a%.eolymp.community.UpdateAccountOutput\"\x1f\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\n\x1a\x08/account\x12\x85\x01\n\rUploadPicture\x12$.eolymp.community.UploadPictureInput\x1a%.eolymp.community.UploadPictureOutput\"\'\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\x12\"\x10/account/picture\x12}\n\rDeleteAccount\x12$.eolymp.community.DeleteAccountInput\x1a%.eolymp.community.DeleteAccountOutput\"\x1f\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\n\x82\xd3\xe4\x93\x02\n*\x08/account\x12\xa0\x01\n\x12ResendVerification\x12).eolymp.community.ResendVerificationInput\x1a*.eolymp.community.ResendVerificationOutput\"3\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\x1e\"\x1c/account/verification/resend\x12\xa8\x01\n\x14\x43ompleteVerification\x12+.eolymp.community.CompleteVerificationInput\x1a,.eolymp.community.CompleteVerificationOutput\"5\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x01\x82\xd3\xe4\x93\x02 \"\x1e/account/verification/complete\x12\x8c\x01\n\rStartRecovery\x12$.eolymp.community.StartRecoveryInput\x1a%.eolymp.community.StartRecoveryOutput\".\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x00@\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\x19\"\x17/account/recovery/start\x12\x96\x01\n\x10\x43ompleteRecovery\x12&.eolymp.community.CompleteRecoverInput\x1a\'.eolymp.community.CompleteRecoverOutput\"1\xea\xe2\n\x0b\xf5\xe2\n\x00\x00 A\xf8\xe2\n2\x82\xd3\xe4\x93\x02\x1c\"\x1a/account/recovery/completeB5Z3github.com/eolymp/go-sdk/eolymp/community;communityb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.community.account_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z3github.com/eolymp/go-sdk/eolymp/community;community'
  _ACCOUNTSERVICE.methods_by_name['CreateAccount']._options = None
  _ACCOUNTSERVICE.methods_by_name['CreateAccount']._serialized_options = b'\352\342\n\013\365\342\n\000\000 A\370\342\n2\202\323\344\223\002\n\"\010/account'
  _ACCOUNTSERVICE.methods_by_name['DescribeAccount']._options = None
  _ACCOUNTSERVICE.methods_by_name['DescribeAccount']._serialized_options = b'\352\342\n\013\365\342\n\000\000 A\370\342\n2\202\323\344\223\002\n\022\010/account'
  _ACCOUNTSERVICE.methods_by_name['UpdateAccount']._options = None
  _ACCOUNTSERVICE.methods_by_name['UpdateAccount']._serialized_options = b'\352\342\n\013\365\342\n\000\000\200?\370\342\n\005\202\323\344\223\002\n\032\010/account'
  _ACCOUNTSERVICE.methods_by_name['UploadPicture']._options = None
  _ACCOUNTSERVICE.methods_by_name['UploadPicture']._serialized_options = b'\352\342\n\013\365\342\n\000\000\200?\370\342\n\005\202\323\344\223\002\022\"\020/account/picture'
  _ACCOUNTSERVICE.methods_by_name['DeleteAccount']._options = None
  _ACCOUNTSERVICE.methods_by_name['DeleteAccount']._serialized_options = b'\352\342\n\013\365\342\n\000\000\200?\370\342\n\n\202\323\344\223\002\n*\010/account'
  _ACCOUNTSERVICE.methods_by_name['ResendVerification']._options = None
  _ACCOUNTSERVICE.methods_by_name['ResendVerification']._serialized_options = b'\352\342\n\013\365\342\n\000\000\200?\370\342\n\005\202\323\344\223\002\036\"\034/account/verification/resend'
  _ACCOUNTSERVICE.methods_by_name['CompleteVerification']._options = None
  _ACCOUNTSERVICE.methods_by_name['CompleteVerification']._serialized_options = b'\352\342\n\013\365\342\n\000\000\200?\370\342\n\001\202\323\344\223\002 \"\036/account/verification/complete'
  _ACCOUNTSERVICE.methods_by_name['StartRecovery']._options = None
  _ACCOUNTSERVICE.methods_by_name['StartRecovery']._serialized_options = b'\352\342\n\013\365\342\n\000\000\000@\370\342\n\005\202\323\344\223\002\031\"\027/account/recovery/start'
  _ACCOUNTSERVICE.methods_by_name['CompleteRecovery']._options = None
  _ACCOUNTSERVICE.methods_by_name['CompleteRecovery']._serialized_options = b'\352\342\n\013\365\342\n\000\000 A\370\342\n2\202\323\344\223\002\034\"\032/account/recovery/complete'
  _CREATEACCOUNTINPUT._serialized_start=158
  _CREATEACCOUNTINPUT._serialized_end=237
  _CREATEACCOUNTOUTPUT._serialized_start=239
  _CREATEACCOUNTOUTPUT._serialized_end=293
  _DESCRIBEACCOUNTINPUT._serialized_start=295
  _DESCRIBEACCOUNTINPUT._serialized_end=317
  _DESCRIBEACCOUNTOUTPUT._serialized_start=320
  _DESCRIBEACCOUNTOUTPUT._serialized_end=473
  _UPDATEACCOUNTINPUT._serialized_start=476
  _UPDATEACCOUNTINPUT._serialized_end=943
  _UPDATEACCOUNTINPUT_PATCH._serialized_start=626
  _UPDATEACCOUNTINPUT_PATCH._serialized_end=943
  _UPDATEACCOUNTOUTPUT._serialized_start=945
  _UPDATEACCOUNTOUTPUT._serialized_end=980
  _UPLOADPICTUREINPUT._serialized_start=982
  _UPLOADPICTUREINPUT._serialized_end=1084
  _UPLOADPICTUREOUTPUT._serialized_start=1086
  _UPLOADPICTUREOUTPUT._serialized_end=1128
  _DELETEACCOUNTINPUT._serialized_start=1130
  _DELETEACCOUNTINPUT._serialized_end=1150
  _DELETEACCOUNTOUTPUT._serialized_start=1152
  _DELETEACCOUNTOUTPUT._serialized_end=1173
  _RESENDVERIFICATIONINPUT._serialized_start=1175
  _RESENDVERIFICATIONINPUT._serialized_end=1200
  _RESENDVERIFICATIONOUTPUT._serialized_start=1202
  _RESENDVERIFICATIONOUTPUT._serialized_end=1228
  _COMPLETEVERIFICATIONINPUT._serialized_start=1230
  _COMPLETEVERIFICATIONINPUT._serialized_end=1290
  _COMPLETEVERIFICATIONOUTPUT._serialized_start=1292
  _COMPLETEVERIFICATIONOUTPUT._serialized_end=1320
  _STARTRECOVERYINPUT._serialized_start=1322
  _STARTRECOVERYINPUT._serialized_end=1390
  _STARTRECOVERYOUTPUT._serialized_start=1392
  _STARTRECOVERYOUTPUT._serialized_end=1446
  _COMPLETERECOVERINPUT._serialized_start=1448
  _COMPLETERECOVERINPUT._serialized_end=1521
  _COMPLETERECOVEROUTPUT._serialized_start=1523
  _COMPLETERECOVEROUTPUT._serialized_end=1546
  _ACCOUNTSERVICE._serialized_start=1549
  _ACCOUNTSERVICE._serialized_end=2846
# @@protoc_insertion_point(module_scope)
