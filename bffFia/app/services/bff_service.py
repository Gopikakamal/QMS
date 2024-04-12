import grpc
import json
from proto.test_pb2 import FIAQuery
from proto.test_pb2_grpc import FiaStatusServiceStub
from util.common_library import build_response


class FiaStatus:
    """
    A class representing the interaction with the FIA Status gRPC service.
    """

    def GetFiaStatus(self, query):
        """
        Retrieves FIA status based on the provided query using gRPC.

        Args:
            query (dict): A dictionary containing the query parameters.

        Returns:
            dict: A dictionary containing the response received
            from the gRPC service.
        """
        try:
            # Initialize gRPC client with the server address
            channel = grpc.insecure_channel("localhost:9000")
            stub = FiaStatusServiceStub(channel)

            # Call the gRPC service
            response = stub.GetFiaStatus(FIAQuery(json=json.dumps(query)))
            print("==========BFF_RESPONSE========", response)

            # Check if response is empty
            if not response:
                return build_response(500, {"error": "Empty response \
                    received"})

            # Parse the JSON response
            response_json = json.loads(response.json)

            # Check the status field
            status = response_json.get("status")
            data = response_json.get("data")

            if status:
                return build_response(200, data)
            else:
                return build_response(500, data)

        except grpc.RpcError as e:
            if isinstance(e, grpc.Call):
                error_message = "gRPC method call failed: " + str(e.details())
                return build_response(500, {"error": error_message})
            else:
                error_message = "gRPC connection error: " + str(e)
                return build_response(500, {"error": error_message})

        except Exception as e:
            return build_response(500, {"error": "Unexpected error:\
                " + str(e)})
