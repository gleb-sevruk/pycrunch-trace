# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\rmessage.proto\"d\n\x0cTraceSession\x12\x1b\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x0b.TraceEvent\x12!\n\x0cstack_frames\x18\x02 \x03(\x0b\x32\x0b.StackFrame\x12\x14\n\x05\x66iles\x18\x03 \x03(\x0b\x32\x05.File\"-\n\x0e\x46ilesInSession\x12\x1b\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x0c.FileContent\"*\n\x0b\x46ileContent\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\x0c\"\xc7\x01\n\nTraceEvent\x12\x12\n\nevent_name\x18\x01 \x01(\t\x12 \n\x06\x63ursor\x18\x02 \x01(\x0b\x32\x10.ExecutionCursor\x12\x10\n\x08stack_id\x18\x03 \x01(\x05\x12#\n\x0finput_variables\x18\x04 \x01(\x0b\x32\n.Variables\x12\x1a\n\x06locals\x18\x05 \x01(\x0b\x32\n.Variables\x12$\n\x10return_variables\x18\x06 \x01(\x0b\x32\n.Variables\x12\n\n\x02ts\x18\x07 \x01(\x02\")\n\tVariables\x12\x1c\n\tvariables\x18\x01 \x03(\x0b\x32\t.Variable\"\'\n\x08Variable\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"D\n\x0f\x45xecutionCursor\x12\x0c\n\x04\x66ile\x18\x01 \x01(\x05\x12\x0c\n\x04line\x18\x02 \x01(\x05\x12\x15\n\rfunction_name\x18\x03 \x01(\t\" \n\x04\x46ile\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04\x66ile\x18\x02 \x01(\t\"^\n\nStackFrame\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04\x66ile\x18\x02 \x01(\x05\x12\x0c\n\x04line\x18\x03 \x01(\x05\x12\x11\n\tparent_id\x18\x04 \x01(\x05\x12\x15\n\rfunction_name\x18\x05 \x01(\tb\x06proto3'
)




_TRACESESSION = _descriptor.Descriptor(
  name='TraceSession',
  full_name='TraceSession',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='events', full_name='TraceSession.events', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stack_frames', full_name='TraceSession.stack_frames', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='files', full_name='TraceSession.files', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=17,
  serialized_end=117,
)


_FILESINSESSION = _descriptor.Descriptor(
  name='FilesInSession',
  full_name='FilesInSession',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='files', full_name='FilesInSession.files', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=119,
  serialized_end=164,
)


_FILECONTENT = _descriptor.Descriptor(
  name='FileContent',
  full_name='FileContent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='FileContent.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='FileContent.content', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=166,
  serialized_end=208,
)


_TRACEEVENT = _descriptor.Descriptor(
  name='TraceEvent',
  full_name='TraceEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='event_name', full_name='TraceEvent.event_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cursor', full_name='TraceEvent.cursor', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stack_id', full_name='TraceEvent.stack_id', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input_variables', full_name='TraceEvent.input_variables', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='locals', full_name='TraceEvent.locals', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='return_variables', full_name='TraceEvent.return_variables', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ts', full_name='TraceEvent.ts', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=211,
  serialized_end=410,
)


_VARIABLES = _descriptor.Descriptor(
  name='Variables',
  full_name='Variables',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='variables', full_name='Variables.variables', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=412,
  serialized_end=453,
)


_VARIABLE = _descriptor.Descriptor(
  name='Variable',
  full_name='Variable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='Variable.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='Variable.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=455,
  serialized_end=494,
)


_EXECUTIONCURSOR = _descriptor.Descriptor(
  name='ExecutionCursor',
  full_name='ExecutionCursor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file', full_name='ExecutionCursor.file', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='line', full_name='ExecutionCursor.line', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='function_name', full_name='ExecutionCursor.function_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=496,
  serialized_end=564,
)


_FILE = _descriptor.Descriptor(
  name='File',
  full_name='File',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='File.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file', full_name='File.file', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=566,
  serialized_end=598,
)


_STACKFRAME = _descriptor.Descriptor(
  name='StackFrame',
  full_name='StackFrame',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='StackFrame.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='file', full_name='StackFrame.file', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='line', full_name='StackFrame.line', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='parent_id', full_name='StackFrame.parent_id', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='function_name', full_name='StackFrame.function_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
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
  serialized_start=600,
  serialized_end=694,
)

_TRACESESSION.fields_by_name['events'].message_type = _TRACEEVENT
_TRACESESSION.fields_by_name['stack_frames'].message_type = _STACKFRAME
_TRACESESSION.fields_by_name['files'].message_type = _FILE
_FILESINSESSION.fields_by_name['files'].message_type = _FILECONTENT
_TRACEEVENT.fields_by_name['cursor'].message_type = _EXECUTIONCURSOR
_TRACEEVENT.fields_by_name['input_variables'].message_type = _VARIABLES
_TRACEEVENT.fields_by_name['locals'].message_type = _VARIABLES
_TRACEEVENT.fields_by_name['return_variables'].message_type = _VARIABLES
_VARIABLES.fields_by_name['variables'].message_type = _VARIABLE
DESCRIPTOR.message_types_by_name['TraceSession'] = _TRACESESSION
DESCRIPTOR.message_types_by_name['FilesInSession'] = _FILESINSESSION
DESCRIPTOR.message_types_by_name['FileContent'] = _FILECONTENT
DESCRIPTOR.message_types_by_name['TraceEvent'] = _TRACEEVENT
DESCRIPTOR.message_types_by_name['Variables'] = _VARIABLES
DESCRIPTOR.message_types_by_name['Variable'] = _VARIABLE
DESCRIPTOR.message_types_by_name['ExecutionCursor'] = _EXECUTIONCURSOR
DESCRIPTOR.message_types_by_name['File'] = _FILE
DESCRIPTOR.message_types_by_name['StackFrame'] = _STACKFRAME
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TraceSession = _reflection.GeneratedProtocolMessageType('TraceSession', (_message.Message,), {
  'DESCRIPTOR' : _TRACESESSION,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:TraceSession)
  })
_sym_db.RegisterMessage(TraceSession)

FilesInSession = _reflection.GeneratedProtocolMessageType('FilesInSession', (_message.Message,), {
  'DESCRIPTOR' : _FILESINSESSION,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:FilesInSession)
  })
_sym_db.RegisterMessage(FilesInSession)

FileContent = _reflection.GeneratedProtocolMessageType('FileContent', (_message.Message,), {
  'DESCRIPTOR' : _FILECONTENT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:FileContent)
  })
_sym_db.RegisterMessage(FileContent)

TraceEvent = _reflection.GeneratedProtocolMessageType('TraceEvent', (_message.Message,), {
  'DESCRIPTOR' : _TRACEEVENT,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:TraceEvent)
  })
_sym_db.RegisterMessage(TraceEvent)

Variables = _reflection.GeneratedProtocolMessageType('Variables', (_message.Message,), {
  'DESCRIPTOR' : _VARIABLES,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:Variables)
  })
_sym_db.RegisterMessage(Variables)

Variable = _reflection.GeneratedProtocolMessageType('Variable', (_message.Message,), {
  'DESCRIPTOR' : _VARIABLE,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:Variable)
  })
_sym_db.RegisterMessage(Variable)

ExecutionCursor = _reflection.GeneratedProtocolMessageType('ExecutionCursor', (_message.Message,), {
  'DESCRIPTOR' : _EXECUTIONCURSOR,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:ExecutionCursor)
  })
_sym_db.RegisterMessage(ExecutionCursor)

File = _reflection.GeneratedProtocolMessageType('File', (_message.Message,), {
  'DESCRIPTOR' : _FILE,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:File)
  })
_sym_db.RegisterMessage(File)

StackFrame = _reflection.GeneratedProtocolMessageType('StackFrame', (_message.Message,), {
  'DESCRIPTOR' : _STACKFRAME,
  '__module__' : 'message_pb2'
  # @@protoc_insertion_point(class_scope:StackFrame)
  })
_sym_db.RegisterMessage(StackFrame)


# @@protoc_insertion_point(module_scope)
