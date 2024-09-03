# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from data_grpc_service.protos import image_data_api_pb2 as data__grpc__service_dot_protos_dot_image__data__api__pb2


class ImageDataApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetImageDataById = channel.unary_stream(
                '/ImageDataApi/GetImageDataById',
                request_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdRequest.SerializeToString,
                response_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdResponse.FromString,
                )


class ImageDataApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetImageDataById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ImageDataApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetImageDataById': grpc.unary_stream_rpc_method_handler(
                    servicer.GetImageDataById,
                    request_deserializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdRequest.FromString,
                    response_serializer=data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ImageDataApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ImageDataApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetImageDataById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/ImageDataApi/GetImageDataById',
            data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdRequest.SerializeToString,
            data__grpc__service_dot_protos_dot_image__data__api__pb2.GetImageDataByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
