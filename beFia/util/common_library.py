from typing import Any, Dict


def response_json(status: bool, data: Dict[str, Any] = None):
    """
    making json data
    Args:
        status (bool): status true/false
        data (list): actual data list or dict

    Returns:
        dict: json response
    """
    # print("=======>>>>>>>>>>>>>>>>>>>>data", data)
    if data is None:
        data = {}
    return {"status": status, "data": data}
