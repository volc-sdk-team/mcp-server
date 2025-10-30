"""
MCP Server Deploy 主入口模块

提供应用程序的主要启动逻辑，包括环境变量加载和服务器启动。
"""

import sys
import logging
from typing import NoReturn

from dotenv import load_dotenv


def setup_logging() -> None:
    """设置日志配置"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )


def main() -> NoReturn:
    """
    应用程序主入口
    
    加载环境变量并启动 MCP 服务器。
    
    Raises:
        SystemExit: 当服务器启动失败时退出
    """
    try:
        # 设置日志
        setup_logging()
        logger = logging.getLogger(__name__)
        
        # 加载.env文件
        logger.info("正在加载环境变量...")
        load_dotenv()
        logger.info("环境变量加载完成")

        # 启动服务器
        logger.info("MCP Server Deploy 启动中...")
        from .server import run_server

        run_server()
        
    except KeyboardInterrupt:
        logger = logging.getLogger(__name__)
        logger.info("收到中断信号，正在关闭服务器...")
        sys.exit(0)
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
