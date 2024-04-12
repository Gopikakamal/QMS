import json
import grpc
from proto.test_pb2 import FIAQuery
from proto.test_pb2_grpc import FiaStatusServiceStub
from util.common_library import build_response


class FiaStatus:
    """
    A class representing interaction with the FIA Status gRPC service for
    updating status.
    """

    server_address = "localhost:9000"

    def UpdateFiaStatus(self, query):
        """
        Updates FIA status based on the provided query using gRPC.

        Args:
            query (dict): A dictionary containing the query parameters.

        Returns:
            dict: A dictionary containing the response received
            from the gRPC service.
        """
        try:
            # Establish gRPC channel with the server
            channel = grpc.insecure_channel(FiaStatus.server_address)
            stub = FiaStatusServiceStub(channel)

            # Call the gRPC service to update FIA status
            response = stub.UpdateFiaStatus(FIAQuery(json=json.dumps(query)))
            print(response)

            # Check if response is empty
            if not response:
                return build_response(500, {"error": "Empty response\
                    received"})

            # Parse JSON response
            response_json = json.loads(response.json)
            status = response_json.get("status")

            # Handle response status
            if status is None:
                return build_response(500, "No Data Found")
            elif status:
                return build_response(200, "Data updated successfully")
            else:
                return build_response(500, "Invalid Response")
        except grpc.RpcError as e:
            # Handle gRPC errors
            error_message = "gRPC method call failed: " + str(e.details())
            return build_response(500, {"error": error_message})
        except Exception as e:
            # Handle other unexpected errors
            return build_response(500, {"error": "Unexpected error: \
                " + str(e)})
