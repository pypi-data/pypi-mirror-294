# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: core/core.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x63ore/core.proto\x12\x0fmavsdk.rpc.core\"!\n\x1fSubscribeConnectionStateRequest\"U\n\x17\x43onnectionStateResponse\x12:\n\x10\x63onnection_state\x18\x01 \x01(\x0b\x32 .mavsdk.rpc.core.ConnectionState\"-\n\x18SetMavlinkTimeoutRequest\x12\x11\n\ttimeout_s\x18\x01 \x01(\x01\"\x1b\n\x19SetMavlinkTimeoutResponse\"\'\n\x0f\x43onnectionState\x12\x14\n\x0cis_connected\x18\x02 \x01(\x08\x32\xf7\x01\n\x0b\x43oreService\x12z\n\x18SubscribeConnectionState\x12\x30.mavsdk.rpc.core.SubscribeConnectionStateRequest\x1a(.mavsdk.rpc.core.ConnectionStateResponse\"\x00\x30\x01\x12l\n\x11SetMavlinkTimeout\x12).mavsdk.rpc.core.SetMavlinkTimeoutRequest\x1a*.mavsdk.rpc.core.SetMavlinkTimeoutResponse\"\x00\x42\x1b\n\x0eio.mavsdk.coreB\tCoreProtob\x06proto3')



_SUBSCRIBECONNECTIONSTATEREQUEST = DESCRIPTOR.message_types_by_name['SubscribeConnectionStateRequest']
_CONNECTIONSTATERESPONSE = DESCRIPTOR.message_types_by_name['ConnectionStateResponse']
_SETMAVLINKTIMEOUTREQUEST = DESCRIPTOR.message_types_by_name['SetMavlinkTimeoutRequest']
_SETMAVLINKTIMEOUTRESPONSE = DESCRIPTOR.message_types_by_name['SetMavlinkTimeoutResponse']
_CONNECTIONSTATE = DESCRIPTOR.message_types_by_name['ConnectionState']
SubscribeConnectionStateRequest = _reflection.GeneratedProtocolMessageType('SubscribeConnectionStateRequest', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBECONNECTIONSTATEREQUEST,
  '__module__' : 'core.core_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.core.SubscribeConnectionStateRequest)
  })
_sym_db.RegisterMessage(SubscribeConnectionStateRequest)

ConnectionStateResponse = _reflection.GeneratedProtocolMessageType('ConnectionStateResponse', (_message.Message,), {
  'DESCRIPTOR' : _CONNECTIONSTATERESPONSE,
  '__module__' : 'core.core_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.core.ConnectionStateResponse)
  })
_sym_db.RegisterMessage(ConnectionStateResponse)

SetMavlinkTimeoutRequest = _reflection.GeneratedProtocolMessageType('SetMavlinkTimeoutRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETMAVLINKTIMEOUTREQUEST,
  '__module__' : 'core.core_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.core.SetMavlinkTimeoutRequest)
  })
_sym_db.RegisterMessage(SetMavlinkTimeoutRequest)

SetMavlinkTimeoutResponse = _reflection.GeneratedProtocolMessageType('SetMavlinkTimeoutResponse', (_message.Message,), {
  'DESCRIPTOR' : _SETMAVLINKTIMEOUTRESPONSE,
  '__module__' : 'core.core_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.core.SetMavlinkTimeoutResponse)
  })
_sym_db.RegisterMessage(SetMavlinkTimeoutResponse)

ConnectionState = _reflection.GeneratedProtocolMessageType('ConnectionState', (_message.Message,), {
  'DESCRIPTOR' : _CONNECTIONSTATE,
  '__module__' : 'core.core_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.core.ConnectionState)
  })
_sym_db.RegisterMessage(ConnectionState)

_CORESERVICE = DESCRIPTOR.services_by_name['CoreService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\016io.mavsdk.coreB\tCoreProto'
  _SUBSCRIBECONNECTIONSTATEREQUEST._serialized_start=36
  _SUBSCRIBECONNECTIONSTATEREQUEST._serialized_end=69
  _CONNECTIONSTATERESPONSE._serialized_start=71
  _CONNECTIONSTATERESPONSE._serialized_end=156
  _SETMAVLINKTIMEOUTREQUEST._serialized_start=158
  _SETMAVLINKTIMEOUTREQUEST._serialized_end=203
  _SETMAVLINKTIMEOUTRESPONSE._serialized_start=205
  _SETMAVLINKTIMEOUTRESPONSE._serialized_end=232
  _CONNECTIONSTATE._serialized_start=234
  _CONNECTIONSTATE._serialized_end=273
  _CORESERVICE._serialized_start=276
  _CORESERVICE._serialized_end=523
# @@protoc_insertion_point(module_scope)
