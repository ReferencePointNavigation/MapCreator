# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: NavigableSpace.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import Coordinates_pb2 as Coordinates__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='NavigableSpace.proto',
  package='referencepoint.proto',
  syntax='proto3',
  serialized_pb=_b('\n\x14NavigableSpace.proto\x12\x14referencepoint.proto\x1a\x11\x43oordinates.proto\"u\n\x0eNavigableSpace\x12\x38\n\routerBoundary\x18\x01 \x03(\x0b\x32!.referencepoint.proto.Coordinates\x12)\n\x05rings\x18\x02 \x03(\x0b\x32\x1a.referencepoint.proto.Ring\":\n\x04Ring\x12\x32\n\x07polygon\x18\x01 \x03(\x0b\x32!.referencepoint.proto.CoordinatesB\x1a\n\x18\x63om.referencepoint.protob\x06proto3')
  ,
  dependencies=[Coordinates__pb2.DESCRIPTOR,])




_NAVIGABLESPACE = _descriptor.Descriptor(
  name='NavigableSpace',
  full_name='referencepoint.proto.NavigableSpace',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='outerBoundary', full_name='referencepoint.proto.NavigableSpace.outerBoundary', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='rings', full_name='referencepoint.proto.NavigableSpace.rings', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=65,
  serialized_end=182,
)


_RING = _descriptor.Descriptor(
  name='Ring',
  full_name='referencepoint.proto.Ring',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='polygon', full_name='referencepoint.proto.Ring.polygon', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=184,
  serialized_end=242,
)

_NAVIGABLESPACE.fields_by_name['outerBoundary'].message_type = Coordinates__pb2._COORDINATES
_NAVIGABLESPACE.fields_by_name['rings'].message_type = _RING
_RING.fields_by_name['polygon'].message_type = Coordinates__pb2._COORDINATES
DESCRIPTOR.message_types_by_name['NavigableSpace'] = _NAVIGABLESPACE
DESCRIPTOR.message_types_by_name['Ring'] = _RING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

NavigableSpace = _reflection.GeneratedProtocolMessageType('NavigableSpace', (_message.Message,), dict(
  DESCRIPTOR = _NAVIGABLESPACE,
  __module__ = 'NavigableSpace_pb2'
  # @@protoc_insertion_point(class_scope:referencepoint.proto.NavigableSpace)
  ))
_sym_db.RegisterMessage(NavigableSpace)

Ring = _reflection.GeneratedProtocolMessageType('Ring', (_message.Message,), dict(
  DESCRIPTOR = _RING,
  __module__ = 'NavigableSpace_pb2'
  # @@protoc_insertion_point(class_scope:referencepoint.proto.Ring)
  ))
_sym_db.RegisterMessage(Ring)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\030com.referencepoint.proto'))
# @@protoc_insertion_point(module_scope)
