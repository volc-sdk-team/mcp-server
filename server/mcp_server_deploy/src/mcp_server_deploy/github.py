from fastmcp import Context
from volcenginesdkcore.universal import UniversalInfo
from volcenginesdkcore.rest import ApiException

from .models import ApiResponse
from .open_api.get_client import get_api_client
from .open_api.utils import get_credentials


def check_repo(
    ctx: Context,
    repo_url: str,
    deploy_id: str | None,
) -> ApiResponse:
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

        # 调用CheckRepo接口
        prompt_info = UniversalInfo(
            method="POST",
            service="deploy_agent",
            version="2018-01-01",
            action="CheckRepo",
            content_type="application/json",
        )
        body = {
            "RepoURL": repo_url,
        }
        if deploy_id is not None:
            body["DeployID"] = deploy_id
        check_resp = api_client.do_call(
            info=prompt_info,
            body=body,
        )
        response = ApiResponse.success(check_resp)
    except ApiException as e:
        response = ApiResponse.error("ERROR", e.body)
    except Exception as e:
        response = ApiResponse.error("ERROR", str(e))
    return response
