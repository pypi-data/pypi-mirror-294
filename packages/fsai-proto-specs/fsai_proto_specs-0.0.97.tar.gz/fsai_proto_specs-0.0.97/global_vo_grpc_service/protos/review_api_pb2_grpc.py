# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from global_vo_grpc_service.protos import review_api_pb2 as global__vo__grpc__service_dot_protos_dot_review__api__pb2


class ReviewApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CacheLastUserQuery = channel.unary_unary(
                '/ReviewApi/CacheLastUserQuery',
                request_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CacheLastUserQueryRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CacheLastUserQueryResponse.FromString,
                )
        self.CreateReview = channel.unary_unary(
                '/ReviewApi/CreateReview',
                request_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CreateReviewRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CreateReviewResponse.FromString,
                )
        self.FindReviewById = channel.unary_unary(
                '/ReviewApi/FindReviewById',
                request_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.FindReviewByIdRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.FindReviewByIdResponse.FromString,
                )
        self.ListReviews = channel.unary_unary(
                '/ReviewApi/ListReviews',
                request_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.ListReviewsRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.ListReviewsResponse.FromString,
                )


class ReviewApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CacheLastUserQuery(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateReview(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindReviewById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListReviews(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ReviewApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CacheLastUserQuery': grpc.unary_unary_rpc_method_handler(
                    servicer.CacheLastUserQuery,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CacheLastUserQueryRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CacheLastUserQueryResponse.SerializeToString,
            ),
            'CreateReview': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateReview,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CreateReviewRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.CreateReviewResponse.SerializeToString,
            ),
            'FindReviewById': grpc.unary_unary_rpc_method_handler(
                    servicer.FindReviewById,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.FindReviewByIdRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.FindReviewByIdResponse.SerializeToString,
            ),
            'ListReviews': grpc.unary_unary_rpc_method_handler(
                    servicer.ListReviews,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.ListReviewsRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_review__api__pb2.ListReviewsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ReviewApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ReviewApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CacheLastUserQuery(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReviewApi/CacheLastUserQuery',
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.CacheLastUserQueryRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.CacheLastUserQueryResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateReview(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReviewApi/CreateReview',
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.CreateReviewRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.CreateReviewResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FindReviewById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReviewApi/FindReviewById',
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.FindReviewByIdRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.FindReviewByIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListReviews(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ReviewApi/ListReviews',
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.ListReviewsRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_review__api__pb2.ListReviewsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
