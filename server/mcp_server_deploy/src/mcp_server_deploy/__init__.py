"""
MCP Server Deploy - 火山引擎部署服务的 MCP 服务器

这是一个基于 FastMCP 构建的服务器，提供部署相关的工具和功能。
"""

__version__ = "0.1.0"
__author__ = "ByteDance"
__description__ = "MCP server for Deploy"

from .__main__ import main
from .server import run_server

__all__ = [
    "main",
    "run_server",
    "__version__",
    "__author__",
    "__description__",
]