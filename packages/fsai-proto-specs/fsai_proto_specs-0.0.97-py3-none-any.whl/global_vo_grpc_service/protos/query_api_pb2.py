# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: global_vo_grpc_service/protos/query_api.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from global_vo_grpc_service.protos import utils_pb2 as global__vo__grpc__service_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-global_vo_grpc_service/protos/query_api.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a)global_vo_grpc_service/protos/utils.proto\"@\n\"DetectionsWithinBoundingBoxRequest\x12\x1a\n\x08geo_bbox\x18\x01 \x01(\x0b\x32\x08.GeoBbox\"\x7f\n\rQueryResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\n\n\x02id\x18\x02 \x01(\x05\x12\x1c\n\tgeo_point\x18\x03 \x01(\x0b\x32\t.GeoPoint\x12\x13\n\x0b\x63\x61tegory_id\x18\x04 \x01(\x05\x12\r\n\x05score\x18\x05 \x01(\x02\"V\n\x0eQueryResponses\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\"\n\ndetections\x18\x02 \x03(\x0b\x32\x0e.QueryResponse\"*\n\x1b\x44\x65tectionsAggregatedRequest\x12\x0b\n\x03wkt\x18\x01 \x01(\t\"\xcc\x03\n\x1c\x44\x65tectionsAggregatedResponse\x12\x14\n\x0c\x64\x65tection_id\x18\x01 \x01(\x05\x12\x1d\n\x15\x64\x65tection_instance_id\x18\x02 \x01(\x05\x12\x0b\n\x03lat\x18\x03 \x01(\x02\x12\x0b\n\x03lon\x18\x04 \x01(\x02\x12\x15\n\rcategory_name\x18\x05 \x01(\t\x12\x15\n\rcategory_enum\x18\x06 \x01(\t\x12\x11\n\tmax_score\x18\x07 \x01(\x02\x12\x18\n\x10\x65stimated_height\x18\x08 \x01(\x02\x12\x15\n\rtotal_sources\x18\t \x01(\x05\x12.\n\nfirst_seen\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12-\n\tlast_seen\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0bvendor_name\x18\r \x01(\t\x12\x11\n\tvendor_id\x18\x0e \x01(\t\x12(\n\x07\x66\x65\x61ture\x18\x0f \x01(\x0b\x32\x17.google.protobuf.Struct\x12+\n\ndebug_data\x18\x10 \x01(\x0b\x32\x17.google.protobuf.Struct\x12\r\n\x05state\x18\x11 \x01(\t\"\xbe\x03\n\"DetectionInstancesForSearchPayload\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08image_id\x18\x02 \x01(\x05\x12\x0e\n\x06height\x18\x03 \x01(\x02\x12\r\n\x05state\x18\x04 \x01(\t\x12\x15\n\rcategory_name\x18\x05 \x01(\t\x12\x1b\n\x08location\x18\x06 \x01(\x0b\x32\t.GeoPoint\x12\x18\n\x10score_normalized\x18\x07 \x01(\x05\x12\x17\n\x0f\x63reated_by_name\x18\x08 \x01(\t\x12\x17\n\x0fupdated_by_name\x18\t \x01(\t\x12.\n\ncreated_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12/\n\x0b\x64\x65tected_at\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05h3_l3\x18\r \x01(\t\x12\r\n\x05h3_l4\x18\x0e \x01(\t\x12\r\n\x05h3_l5\x18\x0f \x01(\t\x12\r\n\x05h3_l7\x18\x10 \x01(\t\x12\x0e\n\x06h3_l11\x18\x11 \x01(\t\"6\n(GetDetectionInstanceByIdForSearchRequest\x12\n\n\x02id\x18\x01 \x01(\x05\":\n,GetDetectionInstanceByIdForClickhouseRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\xab\x03\n)DetectionInstanceByIdForClickhousePayload\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61tegory_id\x18\x02 \x01(\x05\x12\x10\n\x08image_id\x18\x03 \x01(\x05\x12\x0b\n\x03lat\x18\x04 \x01(\x02\x12\x0b\n\x03lon\x18\x05 \x01(\x02\x12\r\n\x05score\x18\x06 \x01(\x02\x12\x0e\n\x06height\x18\x07 \x01(\x02\x12/\n\x0b\x64\x65tected_at\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\ncreated_at\x18\t \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\n \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05state\x18\x0b \x01(\t\x12\x12\n\ncreated_by\x18\x0c \x01(\x05\x12\x12\n\nupdated_by\x18\r \x01(\x05\x12\r\n\x05h3_l3\x18\x0e \x01(\t\x12\r\n\x05h3_l4\x18\x0f \x01(\t\x12\r\n\x05h3_l5\x18\x10 \x01(\t\x12\r\n\x05h3_l7\x18\x11 \x01(\t\x12\x0e\n\x06h3_l11\x18\x12 \x01(\t2\x97\x04\n\x08QueryApi\x12V\n\x1eGetDetectionsWithinBoundingBox\x12#.DetectionsWithinBoundingBoxRequest\x1a\x0f.QueryResponses\x12X\n\x17GetDetectionsAggregated\x12\x1c.DetectionsAggregatedRequest\x1a\x1d.DetectionsAggregatedResponse0\x01\x12s\n!GetDetectionInstanceByIdForSearch\x12).GetDetectionInstanceByIdForSearchRequest\x1a#.DetectionInstancesForSearchPayload\x12_\n\x1eGetDetectionInstancesForSearch\x12\x16.google.protobuf.Empty\x1a#.DetectionInstancesForSearchPayload0\x01\x12\x82\x01\n%GetDetectionInstanceByIdForClickhouse\x12-.GetDetectionInstanceByIdForClickhouseRequest\x1a*.DetectionInstanceByIdForClickhousePayloadb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'global_vo_grpc_service.protos.query_api_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DETECTIONSWITHINBOUNDINGBOXREQUEST._serialized_start=184
  _DETECTIONSWITHINBOUNDINGBOXREQUEST._serialized_end=248
  _QUERYRESPONSE._serialized_start=250
  _QUERYRESPONSE._serialized_end=377
  _QUERYRESPONSES._serialized_start=379
  _QUERYRESPONSES._serialized_end=465
  _DETECTIONSAGGREGATEDREQUEST._serialized_start=467
  _DETECTIONSAGGREGATEDREQUEST._serialized_end=509
  _DETECTIONSAGGREGATEDRESPONSE._serialized_start=512
  _DETECTIONSAGGREGATEDRESPONSE._serialized_end=972
  _DETECTIONINSTANCESFORSEARCHPAYLOAD._serialized_start=975
  _DETECTIONINSTANCESFORSEARCHPAYLOAD._serialized_end=1421
  _GETDETECTIONINSTANCEBYIDFORSEARCHREQUEST._serialized_start=1423
  _GETDETECTIONINSTANCEBYIDFORSEARCHREQUEST._serialized_end=1477
  _GETDETECTIONINSTANCEBYIDFORCLICKHOUSEREQUEST._serialized_start=1479
  _GETDETECTIONINSTANCEBYIDFORCLICKHOUSEREQUEST._serialized_end=1537
  _DETECTIONINSTANCEBYIDFORCLICKHOUSEPAYLOAD._serialized_start=1540
  _DETECTIONINSTANCEBYIDFORCLICKHOUSEPAYLOAD._serialized_end=1967
  _QUERYAPI._serialized_start=1970
  _QUERYAPI._serialized_end=2505
# @@protoc_insertion_point(module_scope)
