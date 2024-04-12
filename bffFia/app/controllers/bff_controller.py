from app.services.bff_service import FiaStatus
# from util.common_library import token_required
# from util.constant import PERMISSION


# @token_required(PERMISSION.get("QUALITY_FPI_VIEW"))
# def GetFiaStatus(is_fpi, tenant_id):
def GetFiaStatus(is_fpi):
    """
    This function retrieves FIA status based on provided parameters.
    Args:
        is_fpi (bool)
        tenant_id
    Returns:
        dict: Response containing FIA status data fetched from the backend.
    """
    query = {"is_fpi": is_fpi}
    bff_service = FiaStatus()
    response = bff_service.GetFiaStatus(query)
    return response
