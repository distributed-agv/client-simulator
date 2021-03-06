# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: guide.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='guide.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0bguide.proto\"\xc5\x01\n\x08\x43\x61rState\x12\x0e\n\x06\x63\x61r_id\x18\x01 \x01(\x05\x12\x0b\n\x03seq\x18\x02 \x01(\x05\x12#\n\x07\x63ur_pos\x18\x03 \x01(\x0b\x32\x12.CarState.Position\x12$\n\x08last_pos\x18\x04 \x01(\x0b\x32\x12.CarState.Position\x12#\n\x07\x64st_pos\x18\x05 \x01(\x0b\x32\x12.CarState.Position\x1a,\n\x08Position\x12\x0f\n\x07row_idx\x18\x01 \x01(\x05\x12\x0f\n\x07\x63ol_idx\x18\x02 \x01(\x05\"z\n\x04Step\x12!\n\tstep_code\x18\x01 \x01(\x0e\x32\x0e.Step.StepCode\"O\n\x08StepCode\x12\x08\n\x04STOP\x10\x00\x12\x08\n\x04LEFT\x10\x01\x12\t\n\x05RIGHT\x10\x02\x12\x0b\n\x07\x46ORWARD\x10\x03\x12\x0c\n\x08\x42\x41\x43KWARD\x10\x04\x12\t\n\x05RESET\x10\x05\x32*\n\x05Guide\x12!\n\x0bGetNextStep\x12\t.CarState\x1a\x05.Step\"\x00\x62\x06proto3'
)



_STEP_STEPCODE = _descriptor.EnumDescriptor(
  name='StepCode',
  full_name='Step.StepCode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STOP', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='LEFT', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RIGHT', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FORWARD', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='BACKWARD', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='RESET', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=258,
  serialized_end=337,
)
_sym_db.RegisterEnumDescriptor(_STEP_STEPCODE)


_CARSTATE_POSITION = _descriptor.Descriptor(
  name='Position',
  full_name='CarState.Position',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='row_idx', full_name='CarState.Position.row_idx', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='col_idx', full_name='CarState.Position.col_idx', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=169,
  serialized_end=213,
)

_CARSTATE = _descriptor.Descriptor(
  name='CarState',
  full_name='CarState',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='car_id', full_name='CarState.car_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='seq', full_name='CarState.seq', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='cur_pos', full_name='CarState.cur_pos', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='last_pos', full_name='CarState.last_pos', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='dst_pos', full_name='CarState.dst_pos', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_CARSTATE_POSITION, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=213,
)


_STEP = _descriptor.Descriptor(
  name='Step',
  full_name='Step',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='step_code', full_name='Step.step_code', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _STEP_STEPCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=215,
  serialized_end=337,
)

_CARSTATE_POSITION.containing_type = _CARSTATE
_CARSTATE.fields_by_name['cur_pos'].message_type = _CARSTATE_POSITION
_CARSTATE.fields_by_name['last_pos'].message_type = _CARSTATE_POSITION
_CARSTATE.fields_by_name['dst_pos'].message_type = _CARSTATE_POSITION
_STEP.fields_by_name['step_code'].enum_type = _STEP_STEPCODE
_STEP_STEPCODE.containing_type = _STEP
DESCRIPTOR.message_types_by_name['CarState'] = _CARSTATE
DESCRIPTOR.message_types_by_name['Step'] = _STEP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CarState = _reflection.GeneratedProtocolMessageType('CarState', (_message.Message,), {

  'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
    'DESCRIPTOR' : _CARSTATE_POSITION,
    '__module__' : 'guide_pb2'
    # @@protoc_insertion_point(class_scope:CarState.Position)
    })
  ,
  'DESCRIPTOR' : _CARSTATE,
  '__module__' : 'guide_pb2'
  # @@protoc_insertion_point(class_scope:CarState)
  })
_sym_db.RegisterMessage(CarState)
_sym_db.RegisterMessage(CarState.Position)

Step = _reflection.GeneratedProtocolMessageType('Step', (_message.Message,), {
  'DESCRIPTOR' : _STEP,
  '__module__' : 'guide_pb2'
  # @@protoc_insertion_point(class_scope:Step)
  })
_sym_db.RegisterMessage(Step)



_GUIDE = _descriptor.ServiceDescriptor(
  name='Guide',
  full_name='Guide',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=339,
  serialized_end=381,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetNextStep',
    full_name='Guide.GetNextStep',
    index=0,
    containing_service=None,
    input_type=_CARSTATE,
    output_type=_STEP,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GUIDE)

DESCRIPTOR.services_by_name['Guide'] = _GUIDE

# @@protoc_insertion_point(module_scope)
