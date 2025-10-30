# coding: utf-8
"""
API调用模块

提供统一的API调用接口，支持多用户认证和连接池复用
"""
import threading
import os

from volcenginesdkcore import UniversalApi, ApiClient, Configuration
from cachetools import LRUCache

# 全局缓存
_api_client_cache_lock = threading.Lock()
_API_CLIENT_CACHE_MAX_SIZE = int(os.getenv("API_CLIENT_CACHE_MAX_SIZE", "128"))
_api_client_cache: LRUCache[str, UniversalApi] = LRUCache(
    maxsize=_API_CLIENT_CACHE_MAX_SIZE
)


def get_api_client(
    ak: str, sk: str, host: str, region: str, token: str = None
) -> UniversalApi:
    configuration = Configuration()

    # 缓存key
    cache_key = f"{host}|{ak}"

    with _api_client_cache_lock:
        if cache_key in _api_client_cache:
            return _api_client_cache[cache_key]

        # 创建新的client并写入缓存
        configuration.ak = ak
        configuration.sk = sk
        configuration.session_token = token
        configuration.host = host
        configuration.region = region
        client = UniversalApi(ApiClient(configuration))

        _api_client_cache[cache_key] = client
        return client
