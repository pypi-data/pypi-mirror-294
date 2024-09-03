# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: log_files/log_files.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import mavsdk_options_pb2 as mavsdk__options__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19log_files/log_files.proto\x12\x14mavsdk.rpc.log_files\x1a\x14mavsdk_options.proto\"\x13\n\x11GetEntriesRequest\"\x82\x01\n\x12GetEntriesResponse\x12>\n\x10log_files_result\x18\x01 \x01(\x0b\x32$.mavsdk.rpc.log_files.LogFilesResult\x12,\n\x07\x65ntries\x18\x02 \x03(\x0b\x32\x1b.mavsdk.rpc.log_files.Entry\"[\n\x1fSubscribeDownloadLogFileRequest\x12*\n\x05\x65ntry\x18\x01 \x01(\x0b\x32\x1b.mavsdk.rpc.log_files.Entry\x12\x0c\n\x04path\x18\x02 \x01(\t\"\x8f\x01\n\x17\x44ownloadLogFileResponse\x12>\n\x10log_files_result\x18\x01 \x01(\x0b\x32$.mavsdk.rpc.log_files.LogFilesResult\x12\x34\n\x08progress\x18\x02 \x01(\x0b\x32\".mavsdk.rpc.log_files.ProgressData\"\x19\n\x17\x45raseAllLogFilesRequest\"Z\n\x18\x45raseAllLogFilesResponse\x12>\n\x10log_files_result\x18\x01 \x01(\x0b\x32$.mavsdk.rpc.log_files.LogFilesResult\")\n\x0cProgressData\x12\x19\n\x08progress\x18\x01 \x01(\x02\x42\x07\x82\xb5\x18\x03NaN\"5\n\x05\x45ntry\x12\n\n\x02id\x18\x01 \x01(\r\x12\x0c\n\x04\x64\x61te\x18\x02 \x01(\t\x12\x12\n\nsize_bytes\x18\x03 \x01(\r\"\xa1\x02\n\x0eLogFilesResult\x12;\n\x06result\x18\x01 \x01(\x0e\x32+.mavsdk.rpc.log_files.LogFilesResult.Result\x12\x12\n\nresult_str\x18\x02 \x01(\t\"\xbd\x01\n\x06Result\x12\x12\n\x0eRESULT_UNKNOWN\x10\x00\x12\x12\n\x0eRESULT_SUCCESS\x10\x01\x12\x0f\n\x0bRESULT_NEXT\x10\x02\x12\x16\n\x12RESULT_NO_LOGFILES\x10\x03\x12\x12\n\x0eRESULT_TIMEOUT\x10\x04\x12\x1b\n\x17RESULT_INVALID_ARGUMENT\x10\x05\x12\x1b\n\x17RESULT_FILE_OPEN_FAILED\x10\x06\x12\x14\n\x10RESULT_NO_SYSTEM\x10\x07\x32\xfc\x02\n\x0fLogFilesService\x12\x61\n\nGetEntries\x12\'.mavsdk.rpc.log_files.GetEntriesRequest\x1a(.mavsdk.rpc.log_files.GetEntriesResponse\"\x00\x12\x8c\x01\n\x18SubscribeDownloadLogFile\x12\x35.mavsdk.rpc.log_files.SubscribeDownloadLogFileRequest\x1a-.mavsdk.rpc.log_files.DownloadLogFileResponse\"\x08\x80\xb5\x18\x00\x88\xb5\x18\x01\x30\x01\x12w\n\x10\x45raseAllLogFiles\x12-.mavsdk.rpc.log_files.EraseAllLogFilesRequest\x1a..mavsdk.rpc.log_files.EraseAllLogFilesResponse\"\x04\x80\xb5\x18\x01\x42$\n\x13io.mavsdk.log_filesB\rLogFilesProtob\x06proto3')



_GETENTRIESREQUEST = DESCRIPTOR.message_types_by_name['GetEntriesRequest']
_GETENTRIESRESPONSE = DESCRIPTOR.message_types_by_name['GetEntriesResponse']
_SUBSCRIBEDOWNLOADLOGFILEREQUEST = DESCRIPTOR.message_types_by_name['SubscribeDownloadLogFileRequest']
_DOWNLOADLOGFILERESPONSE = DESCRIPTOR.message_types_by_name['DownloadLogFileResponse']
_ERASEALLLOGFILESREQUEST = DESCRIPTOR.message_types_by_name['EraseAllLogFilesRequest']
_ERASEALLLOGFILESRESPONSE = DESCRIPTOR.message_types_by_name['EraseAllLogFilesResponse']
_PROGRESSDATA = DESCRIPTOR.message_types_by_name['ProgressData']
_ENTRY = DESCRIPTOR.message_types_by_name['Entry']
_LOGFILESRESULT = DESCRIPTOR.message_types_by_name['LogFilesResult']
_LOGFILESRESULT_RESULT = _LOGFILESRESULT.enum_types_by_name['Result']
GetEntriesRequest = _reflection.GeneratedProtocolMessageType('GetEntriesRequest', (_message.Message,), {
  'DESCRIPTOR' : _GETENTRIESREQUEST,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.GetEntriesRequest)
  })
_sym_db.RegisterMessage(GetEntriesRequest)

GetEntriesResponse = _reflection.GeneratedProtocolMessageType('GetEntriesResponse', (_message.Message,), {
  'DESCRIPTOR' : _GETENTRIESRESPONSE,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.GetEntriesResponse)
  })
_sym_db.RegisterMessage(GetEntriesResponse)

SubscribeDownloadLogFileRequest = _reflection.GeneratedProtocolMessageType('SubscribeDownloadLogFileRequest', (_message.Message,), {
  'DESCRIPTOR' : _SUBSCRIBEDOWNLOADLOGFILEREQUEST,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.SubscribeDownloadLogFileRequest)
  })
_sym_db.RegisterMessage(SubscribeDownloadLogFileRequest)

DownloadLogFileResponse = _reflection.GeneratedProtocolMessageType('DownloadLogFileResponse', (_message.Message,), {
  'DESCRIPTOR' : _DOWNLOADLOGFILERESPONSE,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.DownloadLogFileResponse)
  })
_sym_db.RegisterMessage(DownloadLogFileResponse)

EraseAllLogFilesRequest = _reflection.GeneratedProtocolMessageType('EraseAllLogFilesRequest', (_message.Message,), {
  'DESCRIPTOR' : _ERASEALLLOGFILESREQUEST,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.EraseAllLogFilesRequest)
  })
_sym_db.RegisterMessage(EraseAllLogFilesRequest)

EraseAllLogFilesResponse = _reflection.GeneratedProtocolMessageType('EraseAllLogFilesResponse', (_message.Message,), {
  'DESCRIPTOR' : _ERASEALLLOGFILESRESPONSE,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.EraseAllLogFilesResponse)
  })
_sym_db.RegisterMessage(EraseAllLogFilesResponse)

ProgressData = _reflection.GeneratedProtocolMessageType('ProgressData', (_message.Message,), {
  'DESCRIPTOR' : _PROGRESSDATA,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.ProgressData)
  })
_sym_db.RegisterMessage(ProgressData)

Entry = _reflection.GeneratedProtocolMessageType('Entry', (_message.Message,), {
  'DESCRIPTOR' : _ENTRY,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.Entry)
  })
_sym_db.RegisterMessage(Entry)

LogFilesResult = _reflection.GeneratedProtocolMessageType('LogFilesResult', (_message.Message,), {
  'DESCRIPTOR' : _LOGFILESRESULT,
  '__module__' : 'log_files.log_files_pb2'
  # @@protoc_insertion_point(class_scope:mavsdk.rpc.log_files.LogFilesResult)
  })
_sym_db.RegisterMessage(LogFilesResult)

_LOGFILESSERVICE = DESCRIPTOR.services_by_name['LogFilesService']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023io.mavsdk.log_filesB\rLogFilesProto'
  _PROGRESSDATA.fields_by_name['progress']._options = None
  _PROGRESSDATA.fields_by_name['progress']._serialized_options = b'\202\265\030\003NaN'
  _LOGFILESSERVICE.methods_by_name['SubscribeDownloadLogFile']._options = None
  _LOGFILESSERVICE.methods_by_name['SubscribeDownloadLogFile']._serialized_options = b'\200\265\030\000\210\265\030\001'
  _LOGFILESSERVICE.methods_by_name['EraseAllLogFiles']._options = None
  _LOGFILESSERVICE.methods_by_name['EraseAllLogFiles']._serialized_options = b'\200\265\030\001'
  _GETENTRIESREQUEST._serialized_start=73
  _GETENTRIESREQUEST._serialized_end=92
  _GETENTRIESRESPONSE._serialized_start=95
  _GETENTRIESRESPONSE._serialized_end=225
  _SUBSCRIBEDOWNLOADLOGFILEREQUEST._serialized_start=227
  _SUBSCRIBEDOWNLOADLOGFILEREQUEST._serialized_end=318
  _DOWNLOADLOGFILERESPONSE._serialized_start=321
  _DOWNLOADLOGFILERESPONSE._serialized_end=464
  _ERASEALLLOGFILESREQUEST._serialized_start=466
  _ERASEALLLOGFILESREQUEST._serialized_end=491
  _ERASEALLLOGFILESRESPONSE._serialized_start=493
  _ERASEALLLOGFILESRESPONSE._serialized_end=583
  _PROGRESSDATA._serialized_start=585
  _PROGRESSDATA._serialized_end=626
  _ENTRY._serialized_start=628
  _ENTRY._serialized_end=681
  _LOGFILESRESULT._serialized_start=684
  _LOGFILESRESULT._serialized_end=973
  _LOGFILESRESULT_RESULT._serialized_start=784
  _LOGFILESRESULT_RESULT._serialized_end=973
  _LOGFILESSERVICE._serialized_start=976
  _LOGFILESSERVICE._serialized_end=1356
# @@protoc_insertion_point(module_scope)
