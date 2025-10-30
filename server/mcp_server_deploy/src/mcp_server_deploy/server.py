import os
from typing import Annotated, Optional

from fastmcp import FastMCP, Context
from pydantic import Field

from .knowledge import search_knowledge_api
from .middleware import IdentityMiddleware
from .models import ApiResponse
from .prompt import get_task_openapi
from .terraform import generate_terraform_api
from .todo import create_or_update, update_status, get_list, TodoStatus
from .validate import validate_account_api
from .github import check_repo
from .apig import create_router_session_plugin_impl


# 创建 MCP 服务器
port = int(os.getenv("MCP_SERVER_PORT", "8000"))
host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
mcp = FastMCP(name="Deploy", port=port, host=host)

mcp.add_middleware(IdentityMiddleware())


@mcp.tool(name="get_task", description="获取任务的prompt")
def get_task(
    ctx: Context,
    step: Annotated[str, Field(description="任务步骤")],
    category: Annotated[Optional[str], Field(description="任务类型")] = None,
    deploy_id: Annotated[Optional[str], Field(description="部署ID")] = None,
) -> ApiResponse:
    return get_task_openapi(ctx, step, category, deploy_id)


@mcp.tool(name="validate_account", description="校验火山账号是否实名&余额是否充足")
def validate_account(
    ctx: Context,
) -> ApiResponse:
    return validate_account_api(ctx)


@mcp.tool(name="search_knowledge", description="搜索知识库。出现错误后，优先调用本工具获取解决方案")
def search_knowledge(
    ctx: Context,
    error_msg: Annotated[str, Field(description="错误信息")],
) -> ApiResponse:
    return search_knowledge_api(ctx, error_msg)


# @mcp.tool(
#     name="get_terraform_code",
#     description="生成terraform代码，会保存到项目的 go-volc 目录下",
# )
def get_terraform_code(
    ctx: Context,
    resource_list: Annotated[list[str], Field(description="资源列表")],
    deploy_yaml: Annotated[str, Field(description="go-volc/deploy.yaml的文件内容")],
    current_path: Annotated[
        Optional[str], Field(description="项目当前的路径, 请使用 pwd 命令获取")
    ] = None,
) -> ApiResponse:
    return generate_terraform_api(ctx, resource_list, deploy_yaml, current_path)


@mcp.tool(name="create_or_update_todo", description="创建或更新待办事项")
def create_or_update_todo(
    ctx: Context,
    todos: Annotated[list[str], Field(description="待办事项内容列表")],
    todo_id: Annotated[
        Optional[str], Field(description="待办事项ID, 更新时必传")
    ] = None,
) -> ApiResponse:
    return create_or_update(todos, todo_id)


@mcp.tool(name="finish_todo_item", description="完成待办事项")
def finish_todo_item(
    ctx: Context,
    todo_id: Annotated[str, Field(description="待办事项ID")],
    number: Annotated[int, Field(description="待办事项编号")],
) -> ApiResponse:
    return update_status(todo_id, number, TodoStatus.DONE)


@mcp.tool(name="get_todo_list", description="获取待办事项列表")
def get_todo_list(
    ctx: Context,
    todo_id: Annotated[str, Field(description="待办事项ID")],
) -> ApiResponse:
    return get_list(todo_id)


# @mcp.tool(name="check_repo_permission", description="校验Github项目是否有读仓库的权限")
def check_repo_permission(
    ctx: Context,
    repo_url: Annotated[str, Field(description="项目的Github仓库URL")],
    deploy_id: Annotated[Optional[str], Field(description="部署ID")] = None,
) -> ApiResponse:
    return check_repo(ctx, repo_url, deploy_id)


@mcp.tool(name="create_session_plugin", description="为函数添加 MCP 会话保持插件")
def create_router_session_plugin(
    ctx: Context,
    function_name: Annotated[str, Field(description="VeFaaS 函数名称")]
) -> ApiResponse:
    return create_router_session_plugin_impl(ctx, function_name)

# 使用指定协议启动服务
def run_server():
    transport_mapping = {
        "STDIO": "stdio",
        "SSE": "sse",
        "HTTP": "streamable-http",
    }
    server_mode = os.getenv("MCP_SERVER_MODE", "STDIO").upper()
    transport = transport_mapping.get(server_mode, "stdio")

    try:
        mcp.run(transport=transport)
    except KeyboardInterrupt:
        print("Server stopped.")
