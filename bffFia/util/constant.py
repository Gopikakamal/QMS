from os import getenv


USER_ENDPOINT = getenv("USER_ENDPOINT")

EXTERNAL_URL = {
    "USER_PERMISSION_URL": f"{USER_ENDPOINT}permission/all/token",
    "USER_CHECK_PERMISSION_URL":
        f"{USER_ENDPOINT}authorization/tenant_id/check_permission"
}

# permission
PERMISSION = {
    "OEE_METRICS_VIEW": "com.platform.assetmanagement.asset.manage",
    "QUALITY_FPI_VIEW": "com.qms.inspection.qainspection.all"
}
