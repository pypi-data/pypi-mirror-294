from unittest.mock import patch

import pytest

from milvus_client import MilvusClient

@pytest.fixture
def milvus_client():
    return MilvusClient(uri="http://localhost:19530", token="fake_token")

@pytest.mark.asyncio
async def test_create_collection(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {"collection_name": "test_collection"}
        result = await milvus_client.create_collection(
            {"name": "test_collection"}
        )
        assert result == {"collection_name": "test_collection"}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/collections/create",
            milvus_client.headers,
            {"name": "test_collection"}
        )

@pytest.mark.asyncio
async def test_create_collection_error(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.side_effect = Exception("API Error")
        with pytest.raises(Exception, match="API Error"):
            await milvus_client.create_collection({"name": "test_collection"})

@pytest.mark.asyncio
async def test_load_collection(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {'code': 0, 'data': {}}
        result = await milvus_client.load_collection("test_collection")
        assert result == {'code': 0, 'data': {}}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/collections/load",
            milvus_client.headers,
            {"collectionName": "test_collection", "dbName": None}
        )

@pytest.mark.asyncio
async def test_describe_collection(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {
            "collection_name": "test_collection",
            "fields": []
        }
        result = await milvus_client.describe_collection("test_collection")
        assert result == {"collection_name": "test_collection", "fields": []}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/collections/describe",
            milvus_client.headers,
            {"collectionName": "test_collection", "dbName": None}
        )

@pytest.mark.asyncio
async def test_drop_collection(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {"status": "success"}
        result = await milvus_client.drop_collection("test_collection")
        assert result == {"status": "success"}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/collections/drop",
            milvus_client.headers,
            {"collectionName": "test_collection", "dbName": None}
        )

@pytest.mark.asyncio
async def test_create_partition(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {"partition_name": "test_partition"}
        result = await milvus_client.create_partition(
            "test_collection",
            "test_partition"
        )
        assert result == {"partition_name": "test_partition"}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/partitions/create",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "partitionName": "test_partition"
            }
        )

@pytest.mark.asyncio
async def test_list_partition(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {
            "partition_names": ["partition1", "partition2"]
        }
        result = await milvus_client.list_partition("test_collection")
        assert result == {"partition_names": ["partition1", "partition2"]}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/partitions/list",
            milvus_client.headers,
            {"collectionName": "test_collection"}
        )

@pytest.mark.asyncio
async def test_get_partition_stats(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {"row_count": 1000}
        result = await milvus_client.get_partition_stats(
            "test_collection",
            "test_partition"
        )
        assert result == {"row_count": 1000}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/partitions/get_stats",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "partitionName": "test_partition"
            }
        )

@pytest.mark.asyncio
async def test_search(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = [{"id": 1, "distance": 0.5}]
        result = await milvus_client.search(
            collection_name="test_collection",
            data=[[1.0, 2.0, 3.0]],
            annsField="vector_field"
        )
        assert result == [{"id": 1, "distance": 0.5}]
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/entities/search",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "data": [[1.0, 2.0, 3.0]],
                "annsField": "vector_field",
                "filter": None,
                "limit": 10,
                "outputFields": None,
                "offset": 0,
                "dbName": None,
                "searchParams": None,
                "groupingField": None,
                "partitionNames": None
            }
        )

@pytest.mark.asyncio
async def test_search_with_filter(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = [{"id": 1, "distance": 0.5}]
        result = await milvus_client.search(
            collection_name="test_collection",
            data=[[1.0, 2.0, 3.0]],
            annsField="vector_field",
            filter="id > 100",
            limit=5,
            outputFields=["id", "name"],
            offset=10
        )
        assert result == [{"id": 1, "distance": 0.5}]
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/entities/search",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "data": [[1.0, 2.0, 3.0]],
                "annsField": "vector_field",
                "filter": "id > 100",
                "limit": 5,
                "outputFields": ["id", "name"],
                "offset": 10,
                "dbName": None,
                "searchParams": None,
                "groupingField": None,
                "partitionNames": None
            }
        )

@pytest.mark.asyncio
async def test_get(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = [{"id": 1, "vector": [1.0, 2.0, 3.0]}]
        result = await milvus_client.get(
            collection_name="test_collection",
            ids=[1],
            outputFields=["id", "vector"]
        )
        assert result == [{"id": 1, "vector": [1.0, 2.0, 3.0]}]
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/entities/get",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "id": [1],
                "outputFields": ["id", "vector"],
                "dbName": None,
                "partitionNames": None
            }
        )

@pytest.mark.asyncio
async def test_query(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = [{"id": 1, "name": "test"}]
        result = await milvus_client.query(
            collection_name="test_collection",
            filter="id in [1,2,3]",
            outputFields=["id", "name"]
        )
        assert result == [{"id": 1, "name": "test"}]
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/entities/query",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "filter": "id in [1,2,3]",
                "outputFields": ["id", "name"],
                "limit": None,
                "offset": None,
                "dbName": None,
                "partitionNames": None
            }
        )

@pytest.mark.asyncio
async def test_upsert(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {"upsert_count": 1}
        result = await milvus_client.upsert(
            collection_name="test_collection",
            data=[{"id": 1, "vector": [1.0, 2.0, 3.0]}]
        )
        assert result == {"upsert_count": 1}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/entities/upsert",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "data": [{"id": 1, "vector": [1.0, 2.0, 3.0]}],
                "dbName": None,
                "partitionName": None
            }
        )

@pytest.mark.asyncio
async def test_insert(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {"insert_count": 1}
        result = await milvus_client.insert(
            collection_name="test_collection",
            data=[{"id": 1, "vector": [1.0, 2.0, 3.0]}]
        )
        assert result == {"insert_count": 1}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/entities/insert",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "data": [{"id": 1, "vector": [1.0, 2.0, 3.0]}],
                "dbName": None,
                "partitionName": None
            }
        )

@pytest.mark.asyncio
async def test_delete(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.return_value = {"delete_count": 1}
        result = await milvus_client.delete(
            collection_name="test_collection",
            filter="id in [1,2,3]"
        )
        assert result == {"delete_count": 1}
        mock_post.assert_called_once_with(
            "http://localhost:19530/v2/vectordb/entities/delete",
            milvus_client.headers,
            {
                "collectionName": "test_collection",
                "filter": "id in [1,2,3]",
                "dbName": None,
                "partitionName": None
            }
        )

@pytest.mark.asyncio
async def test_error_handling(milvus_client):
    with patch('milvus_client.MilvusClient.async_post_milvus') as mock_post:
        mock_post.side_effect = Exception("Network error")
        with pytest.raises(Exception, match="Network error"):
            await milvus_client.create_collection({"name": "test_collection"})
