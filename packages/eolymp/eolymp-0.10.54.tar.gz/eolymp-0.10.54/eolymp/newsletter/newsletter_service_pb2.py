# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/newsletter/newsletter_service.proto
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
from eolymp.newsletter import newsletter_pb2 as eolymp_dot_newsletter_dot_newsletter__pb2
from eolymp.wellknown import expression_pb2 as eolymp_dot_wellknown_dot_expression__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*eolymp/newsletter/newsletter_service.proto\x12\x11\x65olymp.newsletter\x1a\x1d\x65olymp/annotations/http.proto\x1a\"eolymp/annotations/ratelimit.proto\x1a\x1e\x65olymp/annotations/scope.proto\x1a\"eolymp/newsletter/newsletter.proto\x1a!eolymp/wellknown/expression.proto\"0\n\x17\x44\x65scribeNewsletterInput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\"M\n\x18\x44\x65scribeNewsletterOutput\x12\x31\n\nnewsletter\x18\x01 \x01(\x0b\x32\x1d.eolymp.newsletter.Newsletter\"4\n\x14ListNewslettersInput\x12\x0e\n\x06offset\x18\n \x01(\x05\x12\x0c\n\x04size\x18\x0b \x01(\x05\"T\n\x15ListNewslettersOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12,\n\x05items\x18\x02 \x03(\x0b\x32\x1d.eolymp.newsletter.Newsletter\"J\n\x15\x43reateNewsletterInput\x12\x31\n\nnewsletter\x18\x01 \x01(\x0b\x32\x1d.eolymp.newsletter.Newsletter\"/\n\x16\x43reateNewsletterOutput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\"\xd6\x01\n\x15UpdateNewsletterInput\x12=\n\x05patch\x18\x01 \x03(\x0e\x32..eolymp.newsletter.UpdateNewsletterInput.Patch\x12\x15\n\rnewsletter_id\x18\x02 \x01(\t\x12\x31\n\nnewsletter\x18\x03 \x01(\x0b\x32\x1d.eolymp.newsletter.Newsletter\"4\n\x05Patch\x12\x07\n\x03\x41LL\x10\x00\x12\x08\n\x04TYPE\x10\x01\x12\x0b\n\x07SUBJECT\x10\x02\x12\x0b\n\x07\x43ONTENT\x10\x03\"\x18\n\x16UpdateNewsletterOutput\".\n\x15\x44\x65leteNewsletterInput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\"\x18\n\x16\x44\x65leteNewsletterOutput\",\n\x13SendNewsletterInput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\"\x16\n\x14SendNewsletterOutput\"K\n\x13TestNewsletterInput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x0e\n\x06locale\x18\x03 \x01(\t\"\x16\n\x14TestNewsletterOutput\"S\n\"DescribeNewsletterTranslationInput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\x12\x16\n\x0etranslation_id\x18\x02 \x01(\t\"e\n#DescribeNewsletterTranslationOutput\x12>\n\x0btranslation\x18\x01 \x01(\x0b\x32).eolymp.newsletter.Newsletter.Translation\"\x99\x02\n\x1fListNewsletterTranslationsInput\x12\x15\n\rnewsletter_id\x18\x02 \x01(\t\x12\x0e\n\x06offset\x18\n \x01(\x05\x12\x0c\n\x04size\x18\x0b \x01(\x05\x12J\n\x07\x66ilters\x18( \x01(\x0b\x32\x39.eolymp.newsletter.ListNewsletterTranslationsInput.Filter\x1au\n\x06\x46ilter\x12\r\n\x05query\x18\x01 \x01(\t\x12*\n\x02id\x18\x02 \x03(\x0b\x32\x1e.eolymp.wellknown.ExpressionID\x12\x30\n\x06locale\x18\x04 \x03(\x0b\x32 .eolymp.wellknown.ExpressionEnum\"k\n ListNewsletterTranslationsOutput\x12\r\n\x05total\x18\x01 \x01(\x05\x12\x38\n\x05items\x18\x02 \x03(\x0b\x32).eolymp.newsletter.Newsletter.Translation\"y\n CreateNewsletterTranslationInput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\x12>\n\x0btranslation\x18\x02 \x01(\x0b\x32).eolymp.newsletter.Newsletter.Translation\";\n!CreateNewsletterTranslationOutput\x12\x16\n\x0etranslation_id\x18\x01 \x01(\t\"\x93\x02\n UpdateNewsletterTranslationInput\x12H\n\x05patch\x18\x01 \x03(\x0e\x32\x39.eolymp.newsletter.UpdateNewsletterTranslationInput.Patch\x12\x15\n\rnewsletter_id\x18\x02 \x01(\t\x12\x16\n\x0etranslation_id\x18\x03 \x01(\t\x12>\n\x0btranslation\x18\x04 \x01(\x0b\x32).eolymp.newsletter.Newsletter.Translation\"6\n\x05Patch\x12\x07\n\x03\x41LL\x10\x00\x12\x0b\n\x07SUBJECT\x10\x01\x12\x0b\n\x07\x43ONTENT\x10\x02\x12\n\n\x06LOCALE\x10\x03\"#\n!UpdateNewsletterTranslationOutput\"Q\n DeleteNewsletterTranslationInput\x12\x15\n\rnewsletter_id\x18\x01 \x01(\t\x12\x16\n\x0etranslation_id\x18\x02 \x01(\t\"#\n!DeleteNewsletterTranslationOutput2\xd6\x13\n\x11NewsletterService\x12\xa2\x01\n\x12\x44\x65scribeNewsletter\x12*.eolymp.newsletter.DescribeNewsletterInput\x1a+.eolymp.newsletter.DescribeNewsletterOutput\"3\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02\x1d\x12\x1b/newsletter/{newsletter_id}\x12\x88\x01\n\x0fListNewsletters\x12\'.eolymp.newsletter.ListNewslettersInput\x1a(.eolymp.newsletter.ListNewslettersOutput\"\"\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\nd\x82\xd3\xe4\x93\x02\r\x12\x0b/newsletter\x12\xae\x01\n\x10\x43reateNewsletter\x12(.eolymp.newsletter.CreateNewsletterInput\x1a).eolymp.newsletter.CreateNewsletterOutput\"E\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x03\x82\xd3\xe4\x93\x02\r\"\x0b/newsletter\x12\xbe\x01\n\x10UpdateNewsletter\x12(.eolymp.newsletter.UpdateNewsletterInput\x1a).eolymp.newsletter.UpdateNewsletterOutput\"U\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x00@\xf8\xe2\n\x05\x82\xd3\xe4\x93\x02\x1d\x1a\x1b/newsletter/{newsletter_id}\x12\xbe\x01\n\x10\x44\x65leteNewsletter\x12(.eolymp.newsletter.DeleteNewsletterInput\x1a).eolymp.newsletter.DeleteNewsletterOutput\"U\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n2\x82\xd3\xe4\x93\x02\x1d*\x1b/newsletter/{newsletter_id}\x12\xbd\x01\n\x0eSendNewsletter\x12&.eolymp.newsletter.SendNewsletterInput\x1a\'.eolymp.newsletter.SendNewsletterOutput\"Z\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x02\x82\xd3\xe4\x93\x02\"\" /newsletter/{newsletter_id}/send\x12\xbd\x01\n\x0eTestNewsletter\x12&.eolymp.newsletter.TestNewsletterInput\x1a\'.eolymp.newsletter.TestNewsletterOutput\"Z\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\x80?\xf8\xe2\n\x02\x82\xd3\xe4\x93\x02\"\" /newsletter/{newsletter_id}/test\x12\x83\x02\n\x1d\x44\x65scribeNewsletterTranslation\x12\x35.eolymp.newsletter.DescribeNewsletterTranslationInput\x1a\x36.eolymp.newsletter.DescribeNewsletterTranslationOutput\"s\x82\xe3\n\x1e\x8a\xe3\n\x1anewsletter:newsletter:read\xea\xe2\n\x0c\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\n\xf4\x03\x82\xd3\xe4\x93\x02;\x12\x39/newsletter/{newsletter_id}/translations/{translation_id}\x12\xe8\x01\n\x1aListNewsletterTranslations\x12\x32.eolymp.newsletter.ListNewsletterTranslationsInput\x1a\x33.eolymp.newsletter.ListNewsletterTranslationsOutput\"a\x82\xe3\n\x1e\x8a\xe3\n\x1anewsletter:newsletter:read\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0\x41\xf8\xe2\nd\x82\xd3\xe4\x93\x02*\x12(/newsletter/{newsletter_id}/translations\x12\xec\x01\n\x1b\x43reateNewsletterTranslation\x12\x33.eolymp.newsletter.CreateNewsletterTranslationInput\x1a\x34.eolymp.newsletter.CreateNewsletterTranslationOutput\"b\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n2\x82\xd3\xe4\x93\x02*\"(/newsletter/{newsletter_id}/translations\x12\xfd\x01\n\x1bUpdateNewsletterTranslation\x12\x33.eolymp.newsletter.UpdateNewsletterTranslationInput\x1a\x34.eolymp.newsletter.UpdateNewsletterTranslationOutput\"s\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n2\x82\xd3\xe4\x93\x02;\x1a\x39/newsletter/{newsletter_id}/translations/{translation_id}\x12\xfd\x01\n\x1b\x44\x65leteNewsletterTranslation\x12\x33.eolymp.newsletter.DeleteNewsletterTranslationInput\x1a\x34.eolymp.newsletter.DeleteNewsletterTranslationOutput\"s\x82\xe3\n\x1f\x8a\xe3\n\x1bnewsletter:newsletter:write\xea\xe2\n\x0b\xf5\xe2\n\x00\x00\xa0@\xf8\xe2\n2\x82\xd3\xe4\x93\x02;*9/newsletter/{newsletter_id}/translations/{translation_id}B7Z5github.com/eolymp/go-sdk/eolymp/newsletter;newsletterb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.newsletter.newsletter_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z5github.com/eolymp/go-sdk/eolymp/newsletter;newsletter'
  _NEWSLETTERSERVICE.methods_by_name['DescribeNewsletter']._options = None
  _NEWSLETTERSERVICE.methods_by_name['DescribeNewsletter']._serialized_options = b'\352\342\n\014\365\342\n\000\000\240A\370\342\n\364\003\202\323\344\223\002\035\022\033/newsletter/{newsletter_id}'
  _NEWSLETTERSERVICE.methods_by_name['ListNewsletters']._options = None
  _NEWSLETTERSERVICE.methods_by_name['ListNewsletters']._serialized_options = b'\352\342\n\013\365\342\n\000\000\240A\370\342\nd\202\323\344\223\002\r\022\013/newsletter'
  _NEWSLETTERSERVICE.methods_by_name['CreateNewsletter']._options = None
  _NEWSLETTERSERVICE.methods_by_name['CreateNewsletter']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\200?\370\342\n\003\202\323\344\223\002\r\"\013/newsletter'
  _NEWSLETTERSERVICE.methods_by_name['UpdateNewsletter']._options = None
  _NEWSLETTERSERVICE.methods_by_name['UpdateNewsletter']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\000@\370\342\n\005\202\323\344\223\002\035\032\033/newsletter/{newsletter_id}'
  _NEWSLETTERSERVICE.methods_by_name['DeleteNewsletter']._options = None
  _NEWSLETTERSERVICE.methods_by_name['DeleteNewsletter']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\240@\370\342\n2\202\323\344\223\002\035*\033/newsletter/{newsletter_id}'
  _NEWSLETTERSERVICE.methods_by_name['SendNewsletter']._options = None
  _NEWSLETTERSERVICE.methods_by_name['SendNewsletter']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\200?\370\342\n\002\202\323\344\223\002\"\" /newsletter/{newsletter_id}/send'
  _NEWSLETTERSERVICE.methods_by_name['TestNewsletter']._options = None
  _NEWSLETTERSERVICE.methods_by_name['TestNewsletter']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\200?\370\342\n\002\202\323\344\223\002\"\" /newsletter/{newsletter_id}/test'
  _NEWSLETTERSERVICE.methods_by_name['DescribeNewsletterTranslation']._options = None
  _NEWSLETTERSERVICE.methods_by_name['DescribeNewsletterTranslation']._serialized_options = b'\202\343\n\036\212\343\n\032newsletter:newsletter:read\352\342\n\014\365\342\n\000\000\240A\370\342\n\364\003\202\323\344\223\002;\0229/newsletter/{newsletter_id}/translations/{translation_id}'
  _NEWSLETTERSERVICE.methods_by_name['ListNewsletterTranslations']._options = None
  _NEWSLETTERSERVICE.methods_by_name['ListNewsletterTranslations']._serialized_options = b'\202\343\n\036\212\343\n\032newsletter:newsletter:read\352\342\n\013\365\342\n\000\000\240A\370\342\nd\202\323\344\223\002*\022(/newsletter/{newsletter_id}/translations'
  _NEWSLETTERSERVICE.methods_by_name['CreateNewsletterTranslation']._options = None
  _NEWSLETTERSERVICE.methods_by_name['CreateNewsletterTranslation']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\240@\370\342\n2\202\323\344\223\002*\"(/newsletter/{newsletter_id}/translations'
  _NEWSLETTERSERVICE.methods_by_name['UpdateNewsletterTranslation']._options = None
  _NEWSLETTERSERVICE.methods_by_name['UpdateNewsletterTranslation']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\240@\370\342\n2\202\323\344\223\002;\0329/newsletter/{newsletter_id}/translations/{translation_id}'
  _NEWSLETTERSERVICE.methods_by_name['DeleteNewsletterTranslation']._options = None
  _NEWSLETTERSERVICE.methods_by_name['DeleteNewsletterTranslation']._serialized_options = b'\202\343\n\037\212\343\n\033newsletter:newsletter:write\352\342\n\013\365\342\n\000\000\240@\370\342\n2\202\323\344\223\002;*9/newsletter/{newsletter_id}/translations/{translation_id}'
  _DESCRIBENEWSLETTERINPUT._serialized_start=235
  _DESCRIBENEWSLETTERINPUT._serialized_end=283
  _DESCRIBENEWSLETTEROUTPUT._serialized_start=285
  _DESCRIBENEWSLETTEROUTPUT._serialized_end=362
  _LISTNEWSLETTERSINPUT._serialized_start=364
  _LISTNEWSLETTERSINPUT._serialized_end=416
  _LISTNEWSLETTERSOUTPUT._serialized_start=418
  _LISTNEWSLETTERSOUTPUT._serialized_end=502
  _CREATENEWSLETTERINPUT._serialized_start=504
  _CREATENEWSLETTERINPUT._serialized_end=578
  _CREATENEWSLETTEROUTPUT._serialized_start=580
  _CREATENEWSLETTEROUTPUT._serialized_end=627
  _UPDATENEWSLETTERINPUT._serialized_start=630
  _UPDATENEWSLETTERINPUT._serialized_end=844
  _UPDATENEWSLETTERINPUT_PATCH._serialized_start=792
  _UPDATENEWSLETTERINPUT_PATCH._serialized_end=844
  _UPDATENEWSLETTEROUTPUT._serialized_start=846
  _UPDATENEWSLETTEROUTPUT._serialized_end=870
  _DELETENEWSLETTERINPUT._serialized_start=872
  _DELETENEWSLETTERINPUT._serialized_end=918
  _DELETENEWSLETTEROUTPUT._serialized_start=920
  _DELETENEWSLETTEROUTPUT._serialized_end=944
  _SENDNEWSLETTERINPUT._serialized_start=946
  _SENDNEWSLETTERINPUT._serialized_end=990
  _SENDNEWSLETTEROUTPUT._serialized_start=992
  _SENDNEWSLETTEROUTPUT._serialized_end=1014
  _TESTNEWSLETTERINPUT._serialized_start=1016
  _TESTNEWSLETTERINPUT._serialized_end=1091
  _TESTNEWSLETTEROUTPUT._serialized_start=1093
  _TESTNEWSLETTEROUTPUT._serialized_end=1115
  _DESCRIBENEWSLETTERTRANSLATIONINPUT._serialized_start=1117
  _DESCRIBENEWSLETTERTRANSLATIONINPUT._serialized_end=1200
  _DESCRIBENEWSLETTERTRANSLATIONOUTPUT._serialized_start=1202
  _DESCRIBENEWSLETTERTRANSLATIONOUTPUT._serialized_end=1303
  _LISTNEWSLETTERTRANSLATIONSINPUT._serialized_start=1306
  _LISTNEWSLETTERTRANSLATIONSINPUT._serialized_end=1587
  _LISTNEWSLETTERTRANSLATIONSINPUT_FILTER._serialized_start=1470
  _LISTNEWSLETTERTRANSLATIONSINPUT_FILTER._serialized_end=1587
  _LISTNEWSLETTERTRANSLATIONSOUTPUT._serialized_start=1589
  _LISTNEWSLETTERTRANSLATIONSOUTPUT._serialized_end=1696
  _CREATENEWSLETTERTRANSLATIONINPUT._serialized_start=1698
  _CREATENEWSLETTERTRANSLATIONINPUT._serialized_end=1819
  _CREATENEWSLETTERTRANSLATIONOUTPUT._serialized_start=1821
  _CREATENEWSLETTERTRANSLATIONOUTPUT._serialized_end=1880
  _UPDATENEWSLETTERTRANSLATIONINPUT._serialized_start=1883
  _UPDATENEWSLETTERTRANSLATIONINPUT._serialized_end=2158
  _UPDATENEWSLETTERTRANSLATIONINPUT_PATCH._serialized_start=2104
  _UPDATENEWSLETTERTRANSLATIONINPUT_PATCH._serialized_end=2158
  _UPDATENEWSLETTERTRANSLATIONOUTPUT._serialized_start=2160
  _UPDATENEWSLETTERTRANSLATIONOUTPUT._serialized_end=2195
  _DELETENEWSLETTERTRANSLATIONINPUT._serialized_start=2197
  _DELETENEWSLETTERTRANSLATIONINPUT._serialized_end=2278
  _DELETENEWSLETTERTRANSLATIONOUTPUT._serialized_start=2280
  _DELETENEWSLETTERTRANSLATIONOUTPUT._serialized_end=2315
  _NEWSLETTERSERVICE._serialized_start=2318
  _NEWSLETTERSERVICE._serialized_end=4836
# @@protoc_insertion_point(module_scope)
