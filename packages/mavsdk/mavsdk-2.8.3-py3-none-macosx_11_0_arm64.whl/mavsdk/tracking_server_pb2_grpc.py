# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import tracking_server_pb2 as tracking__server_dot_tracking__server__pb2


class TrackingServerServiceStub(object):
    """API for an onboard image tracking software.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetTrackingPointStatus = channel.unary_unary(
                '/mavsdk.rpc.tracking_server.TrackingServerService/SetTrackingPointStatus',
                request_serializer=tracking__server_dot_tracking__server__pb2.SetTrackingPointStatusRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.SetTrackingPointStatusResponse.FromString,
                )
        self.SetTrackingRectangleStatus = channel.unary_unary(
                '/mavsdk.rpc.tracking_server.TrackingServerService/SetTrackingRectangleStatus',
                request_serializer=tracking__server_dot_tracking__server__pb2.SetTrackingRectangleStatusRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.SetTrackingRectangleStatusResponse.FromString,
                )
        self.SetTrackingOffStatus = channel.unary_unary(
                '/mavsdk.rpc.tracking_server.TrackingServerService/SetTrackingOffStatus',
                request_serializer=tracking__server_dot_tracking__server__pb2.SetTrackingOffStatusRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.SetTrackingOffStatusResponse.FromString,
                )
        self.SubscribeTrackingPointCommand = channel.unary_stream(
                '/mavsdk.rpc.tracking_server.TrackingServerService/SubscribeTrackingPointCommand',
                request_serializer=tracking__server_dot_tracking__server__pb2.SubscribeTrackingPointCommandRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.TrackingPointCommandResponse.FromString,
                )
        self.SubscribeTrackingRectangleCommand = channel.unary_stream(
                '/mavsdk.rpc.tracking_server.TrackingServerService/SubscribeTrackingRectangleCommand',
                request_serializer=tracking__server_dot_tracking__server__pb2.SubscribeTrackingRectangleCommandRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.TrackingRectangleCommandResponse.FromString,
                )
        self.SubscribeTrackingOffCommand = channel.unary_stream(
                '/mavsdk.rpc.tracking_server.TrackingServerService/SubscribeTrackingOffCommand',
                request_serializer=tracking__server_dot_tracking__server__pb2.SubscribeTrackingOffCommandRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.TrackingOffCommandResponse.FromString,
                )
        self.RespondTrackingPointCommand = channel.unary_unary(
                '/mavsdk.rpc.tracking_server.TrackingServerService/RespondTrackingPointCommand',
                request_serializer=tracking__server_dot_tracking__server__pb2.RespondTrackingPointCommandRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.RespondTrackingPointCommandResponse.FromString,
                )
        self.RespondTrackingRectangleCommand = channel.unary_unary(
                '/mavsdk.rpc.tracking_server.TrackingServerService/RespondTrackingRectangleCommand',
                request_serializer=tracking__server_dot_tracking__server__pb2.RespondTrackingRectangleCommandRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.RespondTrackingRectangleCommandResponse.FromString,
                )
        self.RespondTrackingOffCommand = channel.unary_unary(
                '/mavsdk.rpc.tracking_server.TrackingServerService/RespondTrackingOffCommand',
                request_serializer=tracking__server_dot_tracking__server__pb2.RespondTrackingOffCommandRequest.SerializeToString,
                response_deserializer=tracking__server_dot_tracking__server__pb2.RespondTrackingOffCommandResponse.FromString,
                )


class TrackingServerServiceServicer(object):
    """API for an onboard image tracking software.
    """

    def SetTrackingPointStatus(self, request, context):
        """Set/update the current point tracking status.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetTrackingRectangleStatus(self, request, context):
        """Set/update the current rectangle tracking status.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SetTrackingOffStatus(self, request, context):
        """Set the current tracking status to off.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeTrackingPointCommand(self, request, context):
        """Subscribe to incoming tracking point command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeTrackingRectangleCommand(self, request, context):
        """Subscribe to incoming tracking rectangle command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeTrackingOffCommand(self, request, context):
        """Subscribe to incoming tracking off command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RespondTrackingPointCommand(self, request, context):
        """Respond to an incoming tracking point command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RespondTrackingRectangleCommand(self, request, context):
        """Respond to an incoming tracking rectangle command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RespondTrackingOffCommand(self, request, context):
        """Respond to an incoming tracking off command.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TrackingServerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetTrackingPointStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTrackingPointStatus,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.SetTrackingPointStatusRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.SetTrackingPointStatusResponse.SerializeToString,
            ),
            'SetTrackingRectangleStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTrackingRectangleStatus,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.SetTrackingRectangleStatusRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.SetTrackingRectangleStatusResponse.SerializeToString,
            ),
            'SetTrackingOffStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.SetTrackingOffStatus,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.SetTrackingOffStatusRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.SetTrackingOffStatusResponse.SerializeToString,
            ),
            'SubscribeTrackingPointCommand': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeTrackingPointCommand,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.SubscribeTrackingPointCommandRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.TrackingPointCommandResponse.SerializeToString,
            ),
            'SubscribeTrackingRectangleCommand': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeTrackingRectangleCommand,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.SubscribeTrackingRectangleCommandRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.TrackingRectangleCommandResponse.SerializeToString,
            ),
            'SubscribeTrackingOffCommand': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeTrackingOffCommand,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.SubscribeTrackingOffCommandRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.TrackingOffCommandResponse.SerializeToString,
            ),
            'RespondTrackingPointCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RespondTrackingPointCommand,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.RespondTrackingPointCommandRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.RespondTrackingPointCommandResponse.SerializeToString,
            ),
            'RespondTrackingRectangleCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RespondTrackingRectangleCommand,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.RespondTrackingRectangleCommandRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.RespondTrackingRectangleCommandResponse.SerializeToString,
            ),
            'RespondTrackingOffCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.RespondTrackingOffCommand,
                    request_deserializer=tracking__server_dot_tracking__server__pb2.RespondTrackingOffCommandRequest.FromString,
                    response_serializer=tracking__server_dot_tracking__server__pb2.RespondTrackingOffCommandResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mavsdk.rpc.tracking_server.TrackingServerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TrackingServerService(object):
    """API for an onboard image tracking software.
    """

    @staticmethod
    def SetTrackingPointStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/SetTrackingPointStatus',
            tracking__server_dot_tracking__server__pb2.SetTrackingPointStatusRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.SetTrackingPointStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetTrackingRectangleStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/SetTrackingRectangleStatus',
            tracking__server_dot_tracking__server__pb2.SetTrackingRectangleStatusRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.SetTrackingRectangleStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SetTrackingOffStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/SetTrackingOffStatus',
            tracking__server_dot_tracking__server__pb2.SetTrackingOffStatusRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.SetTrackingOffStatusResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeTrackingPointCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/SubscribeTrackingPointCommand',
            tracking__server_dot_tracking__server__pb2.SubscribeTrackingPointCommandRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.TrackingPointCommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeTrackingRectangleCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/SubscribeTrackingRectangleCommand',
            tracking__server_dot_tracking__server__pb2.SubscribeTrackingRectangleCommandRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.TrackingRectangleCommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SubscribeTrackingOffCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/SubscribeTrackingOffCommand',
            tracking__server_dot_tracking__server__pb2.SubscribeTrackingOffCommandRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.TrackingOffCommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RespondTrackingPointCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/RespondTrackingPointCommand',
            tracking__server_dot_tracking__server__pb2.RespondTrackingPointCommandRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.RespondTrackingPointCommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RespondTrackingRectangleCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/RespondTrackingRectangleCommand',
            tracking__server_dot_tracking__server__pb2.RespondTrackingRectangleCommandRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.RespondTrackingRectangleCommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RespondTrackingOffCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.tracking_server.TrackingServerService/RespondTrackingOffCommand',
            tracking__server_dot_tracking__server__pb2.RespondTrackingOffCommandRequest.SerializeToString,
            tracking__server_dot_tracking__server__pb2.RespondTrackingOffCommandResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
