# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from global_vo_grpc_service.protos import team_member_api_pb2 as global__vo__grpc__service_dot_protos_dot_team__member__api__pb2


class TeamMemberApiStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateTeamMember = channel.unary_unary(
                '/TeamMemberApi/CreateTeamMember',
                request_serializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.CreateTeamMemberRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.CreateTeamMemberResponse.FromString,
                )
        self.DeleteTeamMember = channel.unary_unary(
                '/TeamMemberApi/DeleteTeamMember',
                request_serializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.DeleteTeamMemberRequest.SerializeToString,
                response_deserializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.DeleteTeamMemberResponse.FromString,
                )


class TeamMemberApiServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateTeamMember(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTeamMember(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TeamMemberApiServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateTeamMember': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTeamMember,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.CreateTeamMemberRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.CreateTeamMemberResponse.SerializeToString,
            ),
            'DeleteTeamMember': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTeamMember,
                    request_deserializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.DeleteTeamMemberRequest.FromString,
                    response_serializer=global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.DeleteTeamMemberResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'TeamMemberApi', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TeamMemberApi(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateTeamMember(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TeamMemberApi/CreateTeamMember',
            global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.CreateTeamMemberRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.CreateTeamMemberResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteTeamMember(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/TeamMemberApi/DeleteTeamMember',
            global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.DeleteTeamMemberRequest.SerializeToString,
            global__vo__grpc__service_dot_protos_dot_team__member__api__pb2.DeleteTeamMemberResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
