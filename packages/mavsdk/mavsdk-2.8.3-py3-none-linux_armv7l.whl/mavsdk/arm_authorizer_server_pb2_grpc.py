# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import arm_authorizer_server_pb2 as arm__authorizer__server_dot_arm__authorizer__server__pb2


class ArmAuthorizerServerServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SubscribeArmAuthorization = channel.unary_stream(
                '/mavsdk.rpc.arm_authorizer_server.ArmAuthorizerServerService/SubscribeArmAuthorization',
                request_serializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.SubscribeArmAuthorizationRequest.SerializeToString,
                response_deserializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.ArmAuthorizationResponse.FromString,
                )
        self.AcceptArmAuthorization = channel.unary_unary(
                '/mavsdk.rpc.arm_authorizer_server.ArmAuthorizerServerService/AcceptArmAuthorization',
                request_serializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.AcceptArmAuthorizationRequest.SerializeToString,
                response_deserializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.AcceptArmAuthorizationResponse.FromString,
                )
        self.RejectArmAuthorization = channel.unary_unary(
                '/mavsdk.rpc.arm_authorizer_server.ArmAuthorizerServerService/RejectArmAuthorization',
                request_serializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.RejectArmAuthorizationRequest.SerializeToString,
                response_deserializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.RejectArmAuthorizationResponse.FromString,
                )


class ArmAuthorizerServerServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SubscribeArmAuthorization(self, request, context):
        """Subscribe to arm authorization request messages. Each request received should respond to using RespondArmAuthorization
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AcceptArmAuthorization(self, request, context):
        """Authorize arm for the specific time
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RejectArmAuthorization(self, request, context):
        """Reject arm authorization request
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ArmAuthorizerServerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SubscribeArmAuthorization': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeArmAuthorization,
                    request_deserializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.SubscribeArmAuthorizationRequest.FromString,
                    response_serializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.ArmAuthorizationResponse.SerializeToString,
            ),
            'AcceptArmAuthorization': grpc.unary_unary_rpc_method_handler(
                    servicer.AcceptArmAuthorization,
                    request_deserializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.AcceptArmAuthorizationRequest.FromString,
                    response_serializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.AcceptArmAuthorizationResponse.SerializeToString,
            ),
            'RejectArmAuthorization': grpc.unary_unary_rpc_method_handler(
                    servicer.RejectArmAuthorization,
                    request_deserializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.RejectArmAuthorizationRequest.FromString,
                    response_serializer=arm__authorizer__server_dot_arm__authorizer__server__pb2.RejectArmAuthorizationResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mavsdk.rpc.arm_authorizer_server.ArmAuthorizerServerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ArmAuthorizerServerService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SubscribeArmAuthorization(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mavsdk.rpc.arm_authorizer_server.ArmAuthorizerServerService/SubscribeArmAuthorization',
            arm__authorizer__server_dot_arm__authorizer__server__pb2.SubscribeArmAuthorizationRequest.SerializeToString,
            arm__authorizer__server_dot_arm__authorizer__server__pb2.ArmAuthorizationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AcceptArmAuthorization(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.arm_authorizer_server.ArmAuthorizerServerService/AcceptArmAuthorization',
            arm__authorizer__server_dot_arm__authorizer__server__pb2.AcceptArmAuthorizationRequest.SerializeToString,
            arm__authorizer__server_dot_arm__authorizer__server__pb2.AcceptArmAuthorizationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RejectArmAuthorization(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.arm_authorizer_server.ArmAuthorizerServerService/RejectArmAuthorization',
            arm__authorizer__server_dot_arm__authorizer__server__pb2.RejectArmAuthorizationRequest.SerializeToString,
            arm__authorizer__server_dot_arm__authorizer__server__pb2.RejectArmAuthorizationResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
