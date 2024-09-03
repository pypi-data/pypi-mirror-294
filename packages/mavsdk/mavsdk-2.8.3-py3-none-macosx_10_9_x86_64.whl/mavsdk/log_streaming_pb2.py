# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: log_streaming/log_streaming.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import mavsdk_options_pb2 as mavsdk__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!log_streaming/log_streaming.proto\x12\x18mavsdk.rpc.log_streaming\x1a\x14mavsdk_options.proto\"\x1a\n\x18StartLogStreamingRequest\"g\n\x19StartLogStreamingResponse\x12J\n\x14log_streaming_result\x18\x01 \x01(\x0b\x32,.mavsdk.rpc.log_streaming.LogStreamingResult\"\x19\n\x17StopLogStreamingRequest\"f\n\x18StopLogStreamingResponse\x12J\n\x14log_streaming_result\x18\x01 \x01(\x0b\x32,.mavsdk.rpc.log_streaming.LogStreamingResult\"!\n\x1fSubscribeLogStreamingRawRequest\"Y\n\x17LogStreamingRawResponse\x12>\n\x0blogging_raw\x18\x01 \x01(\x0b\x32).mavsdk.rpc.log_streaming.LogStreamingRaw\"\x1f\n\x0fLogStreamingRaw\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\xab\x02\n\x12LogStreamingResult\x12\x43\n\x06result\x18\x01 \x01(\x0e\x32\x33.mavsdk.rpc.log_streaming.LogStreamingResult.Result\x12\x12\n\nresult_str\x18\x02 \x01(\t\"\xbb\x01\n\x06Result\x12\x12\n\x0eRESULT_SUCCESS\x10\x00\x12\x14\n\x10RESULT_NO_SYSTEM\x10\x01\x12\x1b\n\x17RESULT_CONNECTION_ERROR\x10\x02\x12\x0f\n\x0bRESULT_BUSY\x10\x03\x12\x19\n\x15RESULT_COMMAND_DENIED\x10\x04\x12\x12\n\x0eRESULT_TIMEOUT\x10\x05\x12\x16\n\x12RESULT_UNSUPPORTED\x10\x06\x12\x12\n\x0eRESULT_UNKNOWN\x10\x07\x32\xa5\x03\n\x13LogStreamingService\x12~\n\x11StartLogStreaming\x12\x32.mavsdk.rpc.log_streaming.StartLogStreamingRequest\x1a\x33.mavsdk.rpc.log_streaming.StartLogStreamingResponse\"\x00\x12{\n\x10StopLogStreaming\x12\x31.mavsdk.rpc.log_streaming.StopLogStreamingRequest\x1a\x32.mavsdk.rpc.log_streaming.StopLogStreamingResponse\"\x00\x12\x90\x01\n\x18SubscribeLogStreamingRaw\x12\x39.mavsdk.rpc.log_streaming.SubscribeLogStreamingRawRequest\x1a\x31.mavsdk.rpc.log_streaming.LogStreamingRawResponse\"\x04\x80\xb5\x18\x00\x30\x01\x42,\n\x17io.mavsdk.log_streamingB\x11LogStreamingProtob\x06proto3')



_STARTLOGSTREAMINGREQUEST = DESCRIPTOR.message_types_by_name['StartLogStreamingRequest']
_STARTLOGSTREAMINGRESPONSE = DESCRIPTOR.message_types_by_name['StartLogStreamingResponse']
_STOPLOGSTREAMINGREQUEST = DESCRIPTOR.message_types_by_name['StopLogStreamingRequest']
_STOPLOGSTREAMINGRESPONSE = DESCRIPTOR.message_types_by_name['StopLogStreamingResponse']
_SUBSCRIBELOGSTREAMINGRAWREQUEST = DESCRIPTOR.message_types_by_name['SubscribeLogStreamingRawRequest']
_LOGSTREAMINGRAWRESPONSE = DESCRIPTOR.message_types_by_name['LogStreamingRawResponse']
_LOGSTREAMINGRAW = DESCRIPTOR.message_types_by_name['LogStreamingRaw']
_LOGSTREAMINGRESULT = DESCRIPTOR.message_types_by_name['LogStreamingResult']
_LOGSTREAMINGRESULT_RESULT = _LOGSTREAMINGRESULT.enum_types_by_name['Result']
StartLogStreamingRequest = _reflection.GeneratedProtocolMessageType('StartLogStreamingRequest', (_message.Message,), {
  'DESCRIPTOR' : _STARTLOGSTREAMINGREQUEST,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.StartLogStreamingRequest)
  })
_sym_db.RegisterMessage(StartLogStreamingRequest)

StartLogStreamingResponse = _reflection.GeneratedProtocolMessageType('StartLogStreamingResponse', (_message.Message,), {
  'DESCRIPTOR' : _STARTLOGSTREAMINGRESPONSE,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.StartLogStreamingResponse)
  })
_sym_db.RegisterMessage(StartLogStreamingResponse)

StopLogStreamingRequest = _reflection.GeneratedProtocolMessageType('StopLogStreamingRequest', (_message.Message,), {
  'DESCRIPTOR' : _STOPLOGSTREAMINGREQUEST,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.StopLogStreamingRequest)
  })
_sym_db.RegisterMessage(StopLogStreamingRequest)

StopLogStreamingResponse = _reflection.GeneratedProtocolMessageType('StopLogStreamingResponse', (_message.Message,), {
  'DESCRIPTOR' : _STOPLOGSTREAMINGRESPONSE,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.StopLogStreamingResponse)
  })
_sym_db.RegisterMessage(StopLogStreamingResponse)

SubscribeLogStreamingRawRequest = _reflection.GeneratedProtocolMessageType('SubscribeLogStreamingRawRequest', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBELOGSTREAMINGRAWREQUEST,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.SubscribeLogStreamingRawRequest)
  })
_sym_db.RegisterMessage(SubscribeLogStreamingRawRequest)

LogStreamingRawResponse = _reflection.GeneratedProtocolMessageType('LogStreamingRawResponse', (_message.Message,), {
  'DESCRIPTOR' : _LOGSTREAMINGRAWRESPONSE,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.LogStreamingRawResponse)
  })
_sym_db.RegisterMessage(LogStreamingRawResponse)

LogStreamingRaw = _reflection.GeneratedProtocolMessageType('LogStreamingRaw', (_message.Message,), {
  'DESCRIPTOR' : _LOGSTREAMINGRAW,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.LogStreamingRaw)
  })
_sym_db.RegisterMessage(LogStreamingRaw)

LogStreamingResult = _reflection.GeneratedProtocolMessageType('LogStreamingResult', (_message.Message,), {
  'DESCRIPTOR' : _LOGSTREAMINGRESULT,
  '__module__' : 'log_streaming.log_streaming_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_streaming.LogStreamingResult)
  })
_sym_db.RegisterMessage(LogStreamingResult)

_LOGSTREAMINGSERVICE = DESCRIPTOR.services_by_name['LogStreamingService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027io.mavsdk.log_streamingB\021LogStreamingProto'
  _LOGSTREAMINGSERVICE.methods_by_name['SubscribeLogStreamingRaw']._options = None
  _LOGSTREAMINGSERVICE.methods_by_name['SubscribeLogStreamingRaw']._serialized_options = b'\200\265\030\000'
  _STARTLOGSTREAMINGREQUEST._serialized_start=85
  _STARTLOGSTREAMINGREQUEST._serialized_end=111
  _STARTLOGSTREAMINGRESPONSE._serialized_start=113
  _STARTLOGSTREAMINGRESPONSE._serialized_end=216
  _STOPLOGSTREAMINGREQUEST._serialized_start=218
  _STOPLOGSTREAMINGREQUEST._serialized_end=243
  _STOPLOGSTREAMINGRESPONSE._serialized_start=245
  _STOPLOGSTREAMINGRESPONSE._serialized_end=347
  _SUBSCRIBELOGSTREAMINGRAWREQUEST._serialized_start=349
  _SUBSCRIBELOGSTREAMINGRAWREQUEST._serialized_end=382
  _LOGSTREAMINGRAWRESPONSE._serialized_start=384
  _LOGSTREAMINGRAWRESPONSE._serialized_end=473
  _LOGSTREAMINGRAW._serialized_start=475
  _LOGSTREAMINGRAW._serialized_end=506
  _LOGSTREAMINGRESULT._serialized_start=509
  _LOGSTREAMINGRESULT._serialized_end=808
  _LOGSTREAMINGRESULT_RESULT._serialized_start=621
  _LOGSTREAMINGRESULT_RESULT._serialized_end=808
  _LOGSTREAMINGSERVICE._serialized_start=811
  _LOGSTREAMINGSERVICE._serialized_end=1232
# @@protoc_insertion_point(module_scope)
