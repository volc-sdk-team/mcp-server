# deploy MCP Server

| 版本 |    v1.0.0    |
|:--: |:------------:|
| 描述 | 云部署智能体使用的MCP |
| 分类 |     工具类      |
| 标签 |     云部署      |

## Tools
本 MCP Server 产品提供以下 Tools:


- get_task: 获取任务的prompt
- validate_account: 校验火山账号是否实名&余额是否充足
- search_knowledge: 搜索知识库。出现错误后，优先调用本工具获取解决方案
- create_or_update_todo: 创建或更新待办事项
- finish_todo_item: 完成待办事项
- get_todo_list: 获取待办事项列表
- create_session_plugin: 为函数添加 MCP 会话保持插件

- TagResources: 为用户或角色附加指定标签。
## 可适配平台
方舟，Python，Cursor，Trae

## 服务开通链接
https://console.volcengine.com/deploy/identitymanage


## 系统依赖
- 安装 Python 3.11 或者更高版本
- 安装 uv
### 安装 uv 方法
**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## 安装 MCP-Server
克隆仓库:
```bash
git clone git@github.com:volcengine/mcp-server.git
```
## 运行 MCP-Server 指南
### 环境变量设置
- ak 环境变量名:  VOLCENGINE_ACCESS_KEY
- sk 环境变量名:  VOLCENGINE_SECRET_KEY
- session_token 环境变量名:  VOLCENGINE_ACCESS_SESSION_TOKEN

### 运行

#### 变量说明
- /ABSOLUTE/PATH/TO/PARENT/FOLDER
   - mcp-server-deploy 的代码库目录，例如 /Users/xxx/mcp-server/server/mcp_server_deploy，对应 https://github.com/volcengine/mcp-server/tree/main/server/mcp_server_deploy

#### Run Locally
#### 如果已经下载代码库
```json
{
    "mcpServers": {
        "deploy": {
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/PARENT/FOLDER",
                "run",
                "mcp-server-deploy"
            ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your ak",
                "VOLCENGINE_SECRET_KEY": "your sk",
                "VOLCENGINE_ACCESS_SESSION_TOKEN": "your session token"
          }
        }
    }
}
```
#### 如果没有下载代码库
```json
{
    "mcpServers": {
        "deploy": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/volcengine/mcp-server#subdirectory=server/mcp_server_deploy",
                "mcp-server-deploy"
            ],
            "env": {
                "VOLCENGINE_ACCESS_KEY": "your ak",
                "VOLCENGINE_SECRET_KEY": "your sk",
                "VOLCENGINE_ACCESS_SESSION_TOKEN": "your session token"
            }
        }
    }
}
```

## License
[MIT License](https://github.com/volcengine/mcp-server/blob/main/LICENSE)
