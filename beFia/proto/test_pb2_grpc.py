# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import proto.test_pb2 as test__pb2


class FiaStatusServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFiaStatus = channel.unary_unary(
                '/fia_status.FiaStatusService/GetFiaStatus',
                request_serializer=test__pb2.FIAQuery.SerializeToString,
                response_deserializer=test__pb2.FIAResponse.FromString,
                )
        self.PostFiaStatus = channel.unary_unary(
                '/fia_status.FiaStatusService/PostFiaStatus',
                request_serializer=test__pb2.FIAQuery.SerializeToString,
                response_deserializer=test__pb2.FIAResponse.FromString,
                )
        self.UpdateFiaStatus = channel.unary_unary(
                '/fia_status.FiaStatusService/UpdateFiaStatus',
                request_serializer=test__pb2.FIAQuery.SerializeToString,
                response_deserializer=test__pb2.FIAResponse.FromString,
                )


class FiaStatusServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFiaStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PostFiaStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateFiaStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_FiaStatusServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFiaStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFiaStatus,
                    request_deserializer=test__pb2.FIAQuery.FromString,
                    response_serializer=test__pb2.FIAResponse.SerializeToString,
            ),
            'PostFiaStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.PostFiaStatus,
                    request_deserializer=test__pb2.FIAQuery.FromString,
                    response_serializer=test__pb2.FIAResponse.SerializeToString,
            ),
            'UpdateFiaStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateFiaStatus,
                    request_deserializer=test__pb2.FIAQuery.FromString,
                    response_serializer=test__pb2.FIAResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'fia_status.FiaStatusService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class FiaStatusService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFiaStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fia_status.FiaStatusService/GetFiaStatus',
            test__pb2.FIAQuery.SerializeToString,
            test__pb2.FIAResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PostFiaStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fia_status.FiaStatusService/PostFiaStatus',
            test__pb2.FIAQuery.SerializeToString,
            test__pb2.FIAResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateFiaStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/fia_status.FiaStatusService/UpdateFiaStatus',
            test__pb2.FIAQuery.SerializeToString,
            test__pb2.FIAResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
