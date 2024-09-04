# config/milvus.py
from pymilvus import Connections, Collection
import logging

logger = logging.getLogger(__name__)

async def get_milvus_client(uri: str, token: str):
    connections = Connections()
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