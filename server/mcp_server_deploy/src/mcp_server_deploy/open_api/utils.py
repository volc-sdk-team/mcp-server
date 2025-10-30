import os
from fastmcp import Context

# 定义环境变量名称常量
VOLCENGINE_ACCESS_KEY = "VOLCENGINE_ACCESS_KEY"
VOLCENGINE_SECRET_KEY = "VOLCENGINE_SECRET_KEY"
VOLCENGINE_ACCESS_SESSION_TOKEN = "VOLCENGINE_ACCESS_SESSION_TOKEN"
VOLCENGINE_REGION = "VOLCENGINE_REGION"


def get_credentials(ctx: Context, use_original_ak: bool = False) -> dict[str, str]:
    """
    获取认证信息，优先从context获取，如果为空则从环境变量获取
    """
    # 优先从context获取认证信息
    ak = ctx.get_state("ak")
    sk = ctx.get_state("sk")
    token = ctx.get_state("token")
    region = ctx.get_state("region")

    # 如果context中认证信息为空，则从环境变量获取
    if not ak:
        ak = os.getenv(VOLCENGINE_ACCESS_KEY)
    if not sk:
        sk = os.getenv(VOLCENGINE_SECRET_KEY)
    if not token:
        token = os.getenv(VOLCENGINE_ACCESS_SESSION_TOKEN)
    if not region:
        region = os.getenv(VOLCENGINE_REGION, "cn-beijing")

    return {
        "ak": ak,
        "sk": sk,
        "token": token,
        "region": region,
    }
