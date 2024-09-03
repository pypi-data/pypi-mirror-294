# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import geofence_pb2 as geofence_dot_geofence__pb2


class GeofenceServiceStub(object):
    """Enable setting a geofence.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UploadGeofence = channel.unary_unary(
                '/mavsdk.rpc.geofence.GeofenceService/UploadGeofence',
                request_serializer=geofence_dot_geofence__pb2.UploadGeofenceRequest.SerializeToString,
                response_deserializer=geofence_dot_geofence__pb2.UploadGeofenceResponse.FromString,
                )
        self.ClearGeofence = channel.unary_unary(
                '/mavsdk.rpc.geofence.GeofenceService/ClearGeofence',
                request_serializer=geofence_dot_geofence__pb2.ClearGeofenceRequest.SerializeToString,
                response_deserializer=geofence_dot_geofence__pb2.ClearGeofenceResponse.FromString,
                )


class GeofenceServiceServicer(object):
    """Enable setting a geofence.
    """

    def UploadGeofence(self, request, context):
        """
        Upload geofences.

        Polygon and Circular geofences are uploaded to a drone. Once uploaded, the geofence will remain
        on the drone even if a connection is lost.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearGeofence(self, request, context):
        """
        Clear all geofences saved on the vehicle.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GeofenceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UploadGeofence': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadGeofence,
                    request_deserializer=geofence_dot_geofence__pb2.UploadGeofenceRequest.FromString,
                    response_serializer=geofence_dot_geofence__pb2.UploadGeofenceResponse.SerializeToString,
            ),
            'ClearGeofence': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearGeofence,
                    request_deserializer=geofence_dot_geofence__pb2.ClearGeofenceRequest.FromString,
                    response_serializer=geofence_dot_geofence__pb2.ClearGeofenceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mavsdk.rpc.geofence.GeofenceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GeofenceService(object):
    """Enable setting a geofence.
    """

    @staticmethod
    def UploadGeofence(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.geofence.GeofenceService/UploadGeofence',
            geofence_dot_geofence__pb2.UploadGeofenceRequest.SerializeToString,
            geofence_dot_geofence__pb2.UploadGeofenceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClearGeofence(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mavsdk.rpc.geofence.GeofenceService/ClearGeofence',
            geofence_dot_geofence__pb2.ClearGeofenceRequest.SerializeToString,
            geofence_dot_geofence__pb2.ClearGeofenceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
