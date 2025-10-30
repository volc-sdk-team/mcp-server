from fastmcp import Context
from volcenginesdkcore.universal import UniversalInfo
from volcenginesdkcore.rest import ApiException

from .models import ApiResponse
from .open_api.get_client import get_api_client
from .open_api.utils import get_credentials


def create_router_session_plugin_impl(ctx: Context, function_name: str) -> ApiResponse:
    try:
        # 从context获取认证信息，创建统一的api_client
        credentials = get_credentials(ctx, use_original_ak=True)
        ak = credentials["ak"]
        sk = credentials["sk"]
        token = credentials["token"]
        region = credentials["region"]

        # 初始化api_client
        api_client = get_api_client(
            ak, sk, f"apig.{region}.volcengineapi.com", region, token
        )

        # 先获取 service_id
        gateway_service_resp = list_gateway_service(api_client, function_name)
        if (
            not gateway_service_resp
            or not isinstance(gateway_service_resp, dict)
            or "Items" not in gateway_service_resp
            or not gateway_service_resp["Items"]
            or len(gateway_service_resp["Items"]) < 1
        ):
            return ApiResponse.error("ERROR", f"未找到名为 {function_name} 的网关服务")

        service_id = gateway_service_resp["Items"][0]["Id"]

        # 再获取 router_id
        routes_resp = list_routes(api_client, service_id)
        if (
            not routes_resp
            or "Items" not in routes_resp
            or not routes_resp["Items"]
            or len(routes_resp["Items"]) < 1
        ):
            return ApiResponse.error("ERROR", f"服务 {service_id} 下未找到路由")

        router_id = routes_resp["Items"][0]["Id"]

        # 调用CCreatePluginBinding接口
        plugin_info = UniversalInfo(
            method="POST",
            service="apig",
            version="2021-03-03",
            action="CreatePluginBinding",
            content_type="application/json",
        )
        body = {
            "PluginName": "lua-mcp-stateful-session",
            "Scope": "ROUTE",
            "Target": router_id,
            "Enable": True,
            "PluginConfig": "{}",
        }
        crate_resp = api_client.do_call(
            info=plugin_info,
            body=body,
        )
        response = ApiResponse.success(crate_resp)
    except ApiException as e:
        response = ApiResponse.error("ERROR", e.body)
    except Exception as e:
        response = ApiResponse.error("ERROR", str(e))
    return response


def list_routes(api_client, service_id: str) -> dict:
    try:
        # 调用ListRoutes接口
        list_info = UniversalInfo(
            method="POST",
            service="apig",
            version="2022-11-12",
            action="ListRoutes",
            content_type="application/json",
        )
        body = {"ServiceId": service_id}
        list_resp = api_client.do_call(
            info=list_info,
            body=body,
        )
        return list_resp
    except Exception as e:
        return e


def list_gateway_service(api_client, function_name: str) -> dict:
    try:
        # 调用ListGatewayServices接口
        list_info = UniversalInfo(
            method="POST",
            service="apig",
            version="2021-03-03",
            action="ListGatewayServices",
            content_type="application/json",
        )
        body = {"Filter": {"Name": function_name}}
        list_resp = api_client.do_call(
            info=list_info,
            body=body,
        )
        return list_resp
    except Exception as e:
        return e
