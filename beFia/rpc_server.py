import grpc
from concurrent import futures
from proto.test_pb2_grpc import add_FiaStatusServiceServicer_to_server
from app.services.fia_status_service import FiaStatus


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_FiaStatusServiceServicer_to_server(FiaStatus(), server)
    # server.add_insecure_port(f'[::]:9000')
    server.add_insecure_port("[::]:" + str(9000))
    server.start()
    print("working")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
