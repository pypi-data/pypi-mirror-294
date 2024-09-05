# config/milvus.py
from pymilvus import connections  # type: ignore
import logging

logger = logging.getLogger(__name__)

def get_milvus_client(uri: str, token: str):
    if not uri or not token:
        raise ValueError("ZILLIZ_CLOUD_URI and ZILLIZ_CLOUD_TOKEN must be set")
    connections.connect(
        alias="default",
        uri=uri,
        token=token,
        secure=True
    )
    return connections

def get_milvus_collection(client, collection_name):
    return client.get_collection(collection_name)

def has_collection(client, collection_name):
    return client.has_collection(collection_name)