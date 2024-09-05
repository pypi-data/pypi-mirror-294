import pytest
import aiohttp
from aiohttp import ClientError
from aioresponses import aioresponses

from milvus_client import async_post_milvus

@pytest.mark.asyncio
async def test_async_post_milvus_success():
    with aioresponses() as m:
        m.post(
            'http://localhost/test',
            payload={"code": 0, "data": {"key": "value"}},
            status=200
        )

        url = 'http://localhost/test'
        headers = {'Content-Type': 'application/json'}
        payload = {'query': 'test'}

        response_data = await async_post_milvus(url, headers, payload)
        assert response_data == {"key": "value"}

@pytest.mark.asyncio
async def test_async_post_milvus_failure():
    with aioresponses() as m:
        m.post(
            'http://localhost/test',
            payload={"code": 400, "message": "Error"},
            status=400
        )

        url = 'http://localhost/test'
        headers = {'Content-Type': 'application/json'}
        payload = {'query': 'test'}

        with pytest.raises(ClientError):
            await async_post_milvus(url, headers, payload)

@pytest.mark.asyncio
async def test_async_post_milvus_network_error():
    with aioresponses() as m:
        m.post(
            'http://localhost/test',
            exception=aiohttp.ClientConnectionError("Connection failed")
        )

        url = 'http://localhost/test'
        headers = {'Content-Type': 'application/json'}
        payload = {'query': 'test'}

        with pytest.raises(ClientError):
            await async_post_milvus(url, headers, payload)
