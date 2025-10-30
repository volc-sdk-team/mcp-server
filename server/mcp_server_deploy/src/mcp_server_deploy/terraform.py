import hashlib
from dataclasses import dataclass

import volcenginesdkcore
import volcenginesdkcr
import volcenginesdkecs
import volcenginesdkiam
import yaml
from fastmcp import Context
from volcenginesdkcore.rest import ApiException
from volcenginesdkcore.universal import UniversalInfo

from .models import ApiResponse
from .open_api.get_client import get_api_client
from .open_api.utils import get_credentials

CR_PASSWORD_SALT = "deploy_agent"


@dataclass
class DeployConfig:
    ak: str
    sk: str
    region: str
    project_name: str
    volc_project_name: str


def generate_terraform_api(
    ctx: Context,
    resource_list: list[str],
    deploy_yaml: str,
    project_path: str,
) -> ApiResponse:
    try:
        # 从context获取认证信息
        credentials = get_credentials(ctx)
        ak = credentials["ak"]
        sk = credentials["sk"]
        token = credentials["token"]

        # 初始化api_client
        api_client = get_api_client(
            ak, sk, "deploy-agent.volcengineapi.com", "cn-beijing", token
        )

        user_deploy_conf = parse_user_deploy_conf(deploy_yaml)

        # 调用SearchKnowledge接口
        search_info = UniversalInfo(
            method="POST",
            service="deploy_agent",
            version="2018-01-01",
            action="GenerateTerraform",
            content_type="application/json",
        )
        search_resp = api_client.do_call(
            info=search_info,
            body={
                "Region": user_deploy_conf.region,
                "ZoneID": get_zone_id(
                    user_deploy_conf.ak, user_deploy_conf.sk, user_deploy_conf.region
                ),
                "ProjectName": user_deploy_conf.project_name,
                "VolcProjectName": user_deploy_conf.volc_project_name,
                "Resources": resource_list,
                "CreateNewContainerRegistry": not has_already_create_container_registry(
                    user_deploy_conf.ak,
                    user_deploy_conf.sk,
                    user_deploy_conf.region,
                    user_deploy_conf.volc_project_name,
                ),
                "CrPassword": get_cr_password(
                    user_deploy_conf.ak,
                    user_deploy_conf.sk,
                    user_deploy_conf.region,
                ),
            },
        )

        # 保存到项目的 go-volc 目录下
        with open(f"{project_path}/go-volc/main.tf", "w") as f:
            f.write(search_resp['TerraformScript'])

        response = ApiResponse.success({"Notice":"内容已保存到项目的 go-volc 目录下的 main.tf，请继续下一步"})
    except ApiException as e:
        response = ApiResponse.error("ERROR", e.body)
    except Exception as e:
        response = ApiResponse.error("ERROR", str(e))
    return response


def parse_user_deploy_conf(deploy_yaml: str) -> DeployConfig:
    try:
        v = yaml.safe_load(deploy_yaml).get("volcengine", {})
        user_region = v.get("region")
        user_ak = v.get("access_key")
        user_sk = v.get("secret_key")
        volc_project_name = v.get("project_name")
        project_name = yaml.safe_load(deploy_yaml).get("project_name")
    except yaml.YAMLError as e:
        raise Exception(f"解析deploy_yaml失败: {str(e)}")
    if not all([user_region, user_ak, user_sk]):
        raise Exception(
            "deploy_yaml中缺少region、ak、sk、project_name、volc_project_name"
        )
    return DeployConfig(
        ak=user_ak,
        sk=user_sk,
        region=user_region,
        project_name=project_name,
        volc_project_name=volc_project_name,
    )


def get_zone_id(ak: str, sk: str, region: str) -> str:
    """
    根据region获取zone_id
    """
    configuration = volcenginesdkcore.Configuration()
    configuration.ak = ak
    configuration.sk = sk
    configuration.region = region
    volcenginesdkcore.Configuration.set_default(configuration)

    api_instance = volcenginesdkecs.ECSApi()
    describe_zones_request = volcenginesdkecs.DescribeZonesRequest()
    resp = api_instance.describe_zones(describe_zones_request)
    if resp and resp.zones:
        return resp.zones[0].zone_id
    return ""


def has_already_create_container_registry(
    ak: str, sk: str, region: str, volc_project: str
) -> bool:
    """
    检查项目是否已经创建了容器镜像仓库
    """
    configuration = volcenginesdkcore.Configuration()
    configuration.ak = ak
    configuration.sk = sk
    configuration.region = region
    volcenginesdkcore.Configuration.set_default(configuration)

    api_instance = volcenginesdkcr.CRApi()
    req_filter = volcenginesdkcr.FilterForListRegistriesInput(
        names=["deployagent"],
        projects=[volc_project],
    )
    list_registries_request = volcenginesdkcr.ListRegistriesRequest(
        filter=req_filter,
    )

    resp = api_instance.list_registries(list_registries_request)

    return resp and len(resp.items) > 0


def get_cr_password(ak: str, sk: str, region: str) -> str:
    """
    获取容器镜像仓库密码
    """
    configuration = volcenginesdkcore.Configuration()
    configuration.ak = ak
    configuration.sk = sk
    configuration.region = region
    volcenginesdkcore.Configuration.set_default(configuration)

    api_instance = volcenginesdkiam.IAMApi

    get_user_request = volcenginesdkiam.GetUserRequest(
        access_key_id=ak,
    )

    resp: volcenginesdkiam.GetUserResponse = api_instance.get_user(get_user_request)
    if resp and resp.user:
        user: volcenginesdkiam.UserForGetUserOutput = resp.user
        if user:
            return hashlib.md5(
                f"{str(user.account_id)}_{CR_PASSWORD_SALT}".encode("utf-8")
            ).hexdigest()

    return ""


def md5sum(data: str) -> str:
    """
    计算字符串的md5值
    """
