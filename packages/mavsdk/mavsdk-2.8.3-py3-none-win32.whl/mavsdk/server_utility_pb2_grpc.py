# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import server_utility_pb2 as server__utility_dot_server__utility__pb2


class ServerUtilityServiceStub(object):
    """
    Utility for onboard MAVSDK instances for common "server" tasks.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendStatusText = channel.unary_unary(
                '/mavsdk.rpc.server_utility.ServerUtilityService/SendStatusText',
                request_serializer=server__utility_dot_server__utility__pb2.SendStatusTextRequest.SerializeToString,
                response_deserializer=server__utility_dot_server__utility__pb2.SendStatusTextResponse.FromString,
                )


class ServerUtilityServiceServicer(object):
    """
    Utility for onboard MAVSDK instances for common "server" tasks.
    """

    def SendStatusText(self, request, context):
        """Sends a statustext.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerUtilityServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendStatusText': grpc.unary_unary_rpc_method_handler(
                    servicer.SendStatusText,
                    request_deserializer=server__utility_dot_server__utility__pb2.SendStatusTextRequest.FromString,
                    response_serializer=server__utility_dot_server__utility__pb2.SendStatusTextResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mavsdk.rpc.server_utility.ServerUtilityService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ServerUtilityService(object):
    """
    Utility for onboard MAVSDK instances for common "server" tasks.
    """

    @staticmethod
    def SendStatusText(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.server_utility.ServerUtilityService/SendStatusText',
            server__utility_dot_server__utility__pb2.SendStatusTextRequest.SerializeToString,
            server__utility_dot_server__utility__pb2.SendStatusTextResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
