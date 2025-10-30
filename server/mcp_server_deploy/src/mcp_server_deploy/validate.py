from fastmcp import Context
from volcenginesdkcore.universal import UniversalInfo
from volcenginesdkcore.rest import ApiException

from .models import ApiResponse
from .open_api.get_client import get_api_client
from .open_api.utils import get_credentials


def validate_account_api(ctx: Context) -> ApiResponse:
    try:
        # 从context获取认证信息
        credentials = get_credentials(ctx)
        ak = credentials["ak"]
        sk = credentials["sk"]
        token = credentials["token"]
        # 初始化api_client
        api_client = get_api_client(
            ak, sk, "open.volcengineapi.com", "cn-beijing", token
        )

        # 调用CheckPurchasePermission接口
        verify_info = UniversalInfo(
            method="POST",
            service="deploy_agent",
            version="2018-01-01",
            action="IdentityAndPurchase",
            content_type="application/json",
        )
        verify_resp = api_client.do_call(info=verify_info, body={})
        response = ApiResponse.success(verify_resp)
    except ApiException as e:
        response = ApiResponse.error("ERROR", e.body)
    except Exception as e:
        response = ApiResponse.error("ERROR", str(e))
    return response
