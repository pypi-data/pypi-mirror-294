# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: eolymp/commerce/invoice.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from eolymp.commerce import price_pb2 as eolymp_dot_commerce_dot_price__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1d\x65olymp/commerce/invoice.proto\x12\x0f\x65olymp.commerce\x1a\x1b\x65olymp/commerce/price.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xb6\n\n\x07Invoice\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06number\x18\x02 \x01(\t\x12/\n\x06status\x18\x03 \x01(\x0e\x32\x1f.eolymp.commerce.Invoice.Status\x12\x13\n\x0b\x63ustomer_id\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12:\n\x0c\x66rom_invoice\x18\x06 \x01(\x0b\x32$.eolymp.commerce.Invoice.FromInvoice\x12.\n\ncreated_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\x06\x64ue_at\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x1a\n\x12hosted_invoice_url\x18\x1f \x01(\t\x12\x17\n\x0finvoice_pdf_url\x18  \x01(\t\x12\x10\n\x08\x63urrency\x18\x64 \x01(\t\x12\x12\n\namount_due\x18x \x01(\x05\x12\x13\n\x0b\x61mount_paid\x18y \x01(\x05\x12\x18\n\x10\x61mount_remaining\x18z \x01(\x05\x12\x11\n\x08subtotal\x18\x82\x01 \x01(\x05\x12\x1f\n\x16subtotal_excluding_tax\x18\x83\x01 \x01(\x05\x12\x38\n\x0btax_amounts\x18\x8d\x01 \x03(\x0b\x32\".eolymp.commerce.Invoice.TaxAmount\x12\x0c\n\x03tax\x18\x8c\x01 \x01(\x05\x12\x42\n\x10\x64iscount_amounts\x18\x96\x01 \x03(\x0b\x32\'.eolymp.commerce.Invoice.DiscountAmount\x12\x0e\n\x05total\x18\xc8\x01 \x01(\x05\x12\x1c\n\x13total_excluding_tax\x18\xc9\x01 \x01(\x05\x12-\n\x05items\x18\xe7\x07 \x03(\x0b\x32\x1d.eolymp.commerce.Invoice.Item\x1a\xbf\x02\n\x04Item\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x02 \x01(\t\x12\x10\n\x08quantity\x18\n \x01(\r\x12%\n\x05price\x18\x14 \x01(\x0b\x32\x16.eolymp.commerce.Price\x12\x10\n\x08\x63urrency\x18\x64 \x01(\t\x12\x0e\n\x06\x61mount\x18\x65 \x01(\x05\x12\x1c\n\x14\x61mount_excluding_tax\x18\x66 \x01(\x05\x12!\n\x19unit_amount_excluding_tax\x18g \x01(\x05\x12\x41\n\x10\x64iscount_amounts\x18h \x03(\x0b\x32\'.eolymp.commerce.Invoice.DiscountAmount\x12\x37\n\x0btax_amounts\x18i \x03(\x0b\x32\".eolymp.commerce.Invoice.TaxAmount\x1as\n\tTaxAmount\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x05\x12\x11\n\tinclusive\x18\x02 \x01(\x08\x12\x10\n\x08tax_rate\x18\x03 \x01(\t\x12\x19\n\x11taxability_reason\x18\x04 \x01(\t\x12\x16\n\x0etaxable_amount\x18\n \x01(\x05\x1a\x32\n\x0e\x44iscountAmount\x12\x0e\n\x06\x61mount\x18\x01 \x01(\x05\x12\x10\n\x08\x64iscount\x18\x02 \x01(\t\x1a\x30\n\x0b\x46romInvoice\x12\x10\n\x08relation\x18\x01 \x01(\t\x12\x0f\n\x07invoice\x18\x02 \x01(\t\"X\n\x06Status\x12\x12\n\x0eUNKNOWN_STATUS\x10\x00\x12\t\n\x05\x44RAFT\x10\x01\x12\x08\n\x04OPEN\x10\x02\x12\x08\n\x04PAID\x10\x03\x12\x11\n\rUNCOLLECTIBLE\x10\x04\x12\x08\n\x04VOID\x10\x05\x42\x33Z1github.com/eolymp/go-sdk/eolymp/commerce;commerceb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'eolymp.commerce.invoice_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z1github.com/eolymp/go-sdk/eolymp/commerce;commerce'
  _INVOICE._serialized_start=113
  _INVOICE._serialized_end=1447
  _INVOICE_ITEM._serialized_start=819
  _INVOICE_ITEM._serialized_end=1138
  _INVOICE_TAXAMOUNT._serialized_start=1140
  _INVOICE_TAXAMOUNT._serialized_end=1255
  _INVOICE_DISCOUNTAMOUNT._serialized_start=1257
  _INVOICE_DISCOUNTAMOUNT._serialized_end=1307
  _INVOICE_FROMINVOICE._serialized_start=1309
  _INVOICE_FROMINVOICE._serialized_end=1357
  _INVOICE_STATUS._serialized_start=1359
  _INVOICE_STATUS._serialized_end=1447
# @@protoc_insertion_point(module_scope)
