import connexion
from app.services.updatebff_service import FiaStatus
# from util.common_library import token_required
# from util.constant import PERMISSION


# @token_required(PERMISSION.get("QUALITY_FPI_VIEW"))
def update_bff():
    """
    This function updates FIA status based on provided data.
    Returns:
        dict: Response containing the result of the update operation.
    """
    try:
        # Attempt to retrieve JSON data from the request
        data = connexion.request.json
        # Extract tenant_id and list_of_objects from the data
        # tenant_id = data.get("tenant_id")
        list_of_objects = data.get("data")

        # Instantiate updatebff_service
        updatebff_service = FiaStatus()
        # Call UpdateFiaStatus method with list_of_objects
        response = updatebff_service.UpdateFiaStatus(list_of_objects)
        # Return the response
        return response
    except Exception as e:
        # Return an error response in case of any exceptions
        return {"error": f"An unexpected error occurred: {str(e)}"}, 500
