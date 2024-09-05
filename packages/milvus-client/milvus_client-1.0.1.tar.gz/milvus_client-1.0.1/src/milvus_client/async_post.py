import aiohttp

async def async_post_milvus(url, headers, payload):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url,
                headers=headers,
                json=payload
            ) as response:
                response_json = await response.json()
                if (
                    response.status != 200 or
                    response_json.get('code') not in (0, 200)
                ):
                    raise aiohttp.ClientError(response_json)
                return response_json.get('data')
        except Exception as e:
            raise e
