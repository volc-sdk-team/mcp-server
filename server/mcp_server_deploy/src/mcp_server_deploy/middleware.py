import base64
import json

from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers, get_http_request


class IdentityMiddleware(Middleware):
    async def __call__(self, context: MiddlewareContext, call_next):
        try:
            # 提取身份放到ctx
            headers = get_http_headers()
            authorization = headers.get(
                "authorization",
                "eyJBY2Nlc3NLZXlJZCI6IiIsIlNlY3JldEFjY2Vzc0tleSI6IiIsIlNlc3Npb25Ub2tlbiI6IiJ9",
            ).replace("Bearer ", "")
            # base64 decode
            tokenJson = base64.b64decode(authorization).decode('utf-8')
            # parse token
            token = json.loads(tokenJson)
            # set token to context
            context.fastmcp_context.set_state("ak", token.get("AccessKeyId", ""))
            context.fastmcp_context.set_state("sk", token.get("SecretAccessKey", ""))
            context.fastmcp_context.set_state("token", token.get("SessionToken", ""))

            # 提取请求参数放到ctx
            request = get_http_request()
            region = request.query_params.get("region", "")
            context.fastmcp_context.set_state("region", region)
        except Exception as e:
            # 解析失败时使用空值
            context.fastmcp_context.set_state("ak", "")
            context.fastmcp_context.set_state("sk", "")
            context.fastmcp_context.set_state("token", "")
        print(f"Raw middleware processing: {context.method}")
        result = await call_next(context)
        print(f"Raw middleware completed: {context.method}")
        return result
