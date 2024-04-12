from util.constant import EXTERNAL_URL
from flask import jsonify, make_response
from connexion.exceptions import OAuthProblem
import connexion
from json import dumps as json_dumps
from functools import wraps
from typing import Any, Dict
from requests import (
    post as url_post,
    exceptions as request_except
)


def response_json(status: bool, data: Dict[str, Any] = None):
    """
    making json data
    Args:
        status (bool): status true/false
        data (list): actual data list or dict

    Returns:
        dict: json response
    """
    if data is None:
        data = {}
    return {"status": status, "data": data}


def build_response(
        http_status: int, data: Dict[str, Any]) -> make_response:
    """making response structure as common

    Args:
        code (int): status code
        data (Dict): actual data list or dict

    Returns:
        dict: Api response
    """
    resp = data if http_status >= 200 \
        and http_status <= 204 else {"error": data}
    return (
        make_response(jsonify(resp), http_status)
        if data
        else make_response('', http_status)
    )


def bearer_info_func(auth_token=None):
    """
    Method to decode jwt token
    Not required to decode here, external user api will handle those
    validation
    """
    print("=============")
    return {}


def token_required(scope):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            headers = connexion.request.headers.get(
                'Authorization', 'Bearer sample').split(" ")[1]

            # print(headers)
            headers = {
                "Authorization": headers, 'Content-Type': 'application/json'
            }
            response_url = EXTERNAL_URL.get(
                "USER_CHECK_PERMISSION_URL").replace(
                    'tenant_id', kwargs.get("tenant_id")
            )
            payload = json_dumps({"permissionToCheck": scope})
            print("=====", payload)
            try:
                response = url_post(
                    response_url, headers=headers, data=payload)
                print("======resp====", response.json())
            except request_except.RequestException as e:
                raise OAuthProblem(e)
            response_json = response.json()
            if "error" in response_json:
                raise OAuthProblem(response_json.get("error"))
            return func(*args, **kwargs)
        return wrapper
    return decorator
