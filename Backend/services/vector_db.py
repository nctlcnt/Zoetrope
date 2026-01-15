# 向量数据库服务
# 用于媒体条目的语义检索和去重

from abc import ABC, abstractmethod
from typing import Optional
from functools import lru_cache

from ..config import settings


class VectorDBError(Exception):
    """向量数据库错误"""
    pass


class BaseVectorDB(ABC):
    """向量数据库抽象基类"""

    @abstractmethod
    async def init(self) -> None:
        """初始化连接"""
        pass

    @abstractmethod
    async def close(self) -> None:
        """关闭连接"""
        pass

    @abstractmethod
    async def upsert(
        self,
        id: str,
        vector: list[float],
        metadata: dict,
    ) -> None:
        """插入或更新向量"""
        pass

    @abstractmethod
    async def search(
        self,
        vector: list[float],
        top_k: int = 10,
        filter: Optional[dict] = None,
    ) -> list[dict]:
        """
        向量相似度搜索

        Returns:
            [{"id": "xxx", "score": 0.95, "metadata": {...}}, ...]
        """
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """删除向量"""
        pass


class ChromaVectorDB(BaseVectorDB):
    """
    Chroma 向量数据库实现

    适合本地开发和小规模部署
    文档: https://www.trychroma.com/
    """

    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        self._client = None
        self._collection = None

    async def init(self) -> None:
        """
        初始化 Chroma 客户端

        TODO: 实现具体逻辑
        """
        raise NotImplementedError("TODO: 实现 Chroma 初始化")

    async def close(self) -> None:
        """关闭连接"""
        pass  # Chroma 无需显式关闭

    async def upsert(
        self,
        id: str,
        vector: list[float],
        metadata: dict,
    ) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Chroma upsert")

    async def search(
        self,
        vector: list[float],
        top_k: int = 10,
        filter: Optional[dict] = None,
    ) -> list[dict]:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Chroma search")

    async def delete(self, id: str) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Chroma delete")


class PineconeVectorDB(BaseVectorDB):
    """
    Pinecone 向量数据库实现

    适合生产环境大规模部署
    文档: https://www.pinecone.io/
    """

    def __init__(self, api_key: str, environment: str, index_name: str):
        self.api_key = api_key
        self.environment = environment
        self.index_name = index_name
        self._index = None

    async def init(self) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Pinecone 初始化")

    async def close(self) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Pinecone 关闭")

    async def upsert(
        self,
        id: str,
        vector: list[float],
        metadata: dict,
    ) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Pinecone upsert")

    async def search(
        self,
        vector: list[float],
        top_k: int = 10,
        filter: Optional[dict] = None,
    ) -> list[dict]:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Pinecone search")

    async def delete(self, id: str) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Pinecone delete")


class WeaviateVectorDB(BaseVectorDB):
    """
    Weaviate 向量数据库实现

    文档: https://weaviate.io/
    """

    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key
        self._client = None

    async def init(self) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Weaviate 初始化")

    async def close(self) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Weaviate 关闭")

    async def upsert(
        self,
        id: str,
        vector: list[float],
        metadata: dict,
    ) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Weaviate upsert")

    async def search(
        self,
        vector: list[float],
        top_k: int = 10,
        filter: Optional[dict] = None,
    ) -> list[dict]:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Weaviate search")

    async def delete(self, id: str) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Weaviate delete")


class MilvusVectorDB(BaseVectorDB):
    """
    Milvus 向量数据库实现

    文档: https://milvus.io/
    """

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self._client = None

    async def init(self) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Milvus 初始化")

    async def close(self) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Milvus 关闭")

    async def upsert(
        self,
        id: str,
        vector: list[float],
        metadata: dict,
    ) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Milvus upsert")

    async def search(
        self,
        vector: list[float],
        top_k: int = 10,
        filter: Optional[dict] = None,
    ) -> list[dict]:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Milvus search")

    async def delete(self, id: str) -> None:
        """TODO: 实现具体逻辑"""
        raise NotImplementedError("TODO: 实现 Milvus delete")


def create_vector_db() -> BaseVectorDB:
    """
    根据配置创建向量数据库实例

    Returns:
        对应 provider 的向量数据库实例
    """
    provider = settings.vector_db_provider.lower()

    if provider == "chroma":
        return ChromaVectorDB(
            persist_directory=settings.chroma_persist_directory,
        )
    elif provider == "pinecone":
        return PineconeVectorDB(
            api_key=settings.pinecone_api_key,
            environment=settings.pinecone_environment,
            index_name=settings.pinecone_index_name,
        )
    elif provider == "weaviate":
        return WeaviateVectorDB(
            url=settings.weaviate_url,
            api_key=settings.weaviate_api_key,
        )
    elif provider == "milvus":
        return MilvusVectorDB(
            host=settings.milvus_host,
            port=settings.milvus_port,
        )
    else:
        raise ValueError(f"Unsupported vector DB provider: {provider}")


# 全局实例
_vector_db: Optional[BaseVectorDB] = None


async def get_vector_db() -> BaseVectorDB:
    """获取向量数据库实例（依赖注入用）"""
    global _vector_db
    if _vector_db is None:
        _vector_db = create_vector_db()
        await _vector_db.init()
    return _vector_db


async def close_vector_db() -> None:
    """关闭向量数据库连接"""
    global _vector_db
    if _vector_db:
        await _vector_db.close()
        _vector_db = None
