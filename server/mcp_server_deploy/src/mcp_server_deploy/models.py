from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class ErrorInfo:
    """错误信息结构"""

    Code: str = ""
    Message: str = ""


@dataclass
class ApiResponse:
    """统一的API响应结构"""

    Result: Dict[str, Any] = field(default_factory=dict)
    Error: ErrorInfo = field(default_factory=ErrorInfo)

    @classmethod
    def success(cls, data: Dict[str, Any]) -> "ApiResponse":
        """创建成功响应"""
        return cls(Result=data, Error=ErrorInfo(Code="success"))

    @classmethod
    def error(
        cls, code: str, message: str, data: Optional[Dict[str, Any]] = None
    ) -> "ApiResponse":
        """创建错误响应"""
        return cls(Result=data or {}, Error=ErrorInfo(Code=code, Message=message))


@dataclass
class CrConfig:
    id: str = ""
    domain: str = ""
    namespace: str = ""
    repository: str = ""
    tag: str = ""


@dataclass
class VkeConfig:
    id: str = ""


@dataclass
class GitConfig:
    remote_url: str = ""
    branch: str = ""


@dataclass
class DeployConfig:
    region: str = ""
    access_key: str = ""
    secret_key: str = ""
    vke: VkeConfig = field(default_factory=VkeConfig)
    cr: CrConfig = field(default_factory=CrConfig)
    git: GitConfig = field(default_factory=GitConfig)
    deploy_resource_id: str = ""
