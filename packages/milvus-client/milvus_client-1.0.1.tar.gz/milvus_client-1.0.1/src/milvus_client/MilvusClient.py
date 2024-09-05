from .async_post import async_post_milvus

class MilvusClient():
    def __init__(self, uri, token):
        self.base_url = f"{uri}/v2/vectordb/"
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

    async def __post_execute(self, url, payload):
        return await async_post_milvus(url, self.headers, payload)

    async def create_collection(
        self,
        collection_config: dict
    ) -> dict:
        url = self.base_url + "collections/create"
        return await self.__post_execute(url, collection_config)

    async def load_collection(
        self,
        collection_name: str,
        db_name: str = None
    ) -> dict:
        url = self.base_url + "collections/load"
        payload = {
            "collectionName": collection_name,
            "dbName": db_name
        }
        return await self.__post_execute(url, payload)

    async def describe_collection(
        self,
        collection_name: str,
        db_name: str = None
    ) -> dict:
        url = self.base_url + "collections/describe"
        payload = {
            "collectionName": collection_name,
            "dbName": db_name
        }
        return await self.__post_execute(url, payload)

    async def drop_collection(
        self,
        collection_name: str,
        db_name: str = None
    ) -> dict:
        url = self.base_url + "collections/drop"
        payload = {
            "collectionName": collection_name,
            "dbName": db_name
        }
        return await self.__post_execute(url, payload)

    async def create_partition(
        self,
        collection_name: str,
        partition_name: str
    ) -> dict:
        url = self.base_url + "partitions/create"
        payload = {
            "collectionName": collection_name,
            "partitionName": partition_name
        }
        return await self.__post_execute(url, payload)

    async def list_partition(
        self,
        collection_name: str
    ) -> dict:
        url = self.base_url + "partitions/list"
        payload = {
            "collectionName": collection_name
        }
        return await self.__post_execute(url, payload)

    async def get_partition_stats(
        self,
        collection_name: str,
        partition_name: str
    ) -> dict:
        url = self.base_url + "partitions/get_stats"
        payload = {
            "collectionName": collection_name,
            "partitionName": partition_name
        }
        return await self.__post_execute(url, payload)

    async def search(
        self,
        collection_name: str,
        data: list[list],
        annsField: str,
        filter: str = None,
        limit: int = 10,
        outputFields: list = None,
        offset: int = 0,
        db_name: str = None,
        search_params: dict = None,
        grouping_field: str = None,
        partition_names: list = None
    ) -> list[dict]:
        # pylint: disable=too-many-arguments, redefined-builtin
        url = self.base_url + "entities/search"
        payload = {
            "collectionName": collection_name,
            "data": data,
            "annsField": annsField,
            "filter": filter,
            "limit": limit,
            "outputFields": outputFields,
            "offset": offset,
            "dbName": db_name,
            "searchParams": search_params,
            "groupingField": grouping_field,
            "partitionNames": partition_names
        }
        return await self.__post_execute(url, payload)

    async def get(
        self,
        collection_name: str,
        ids: list,
        outputFields: list = None,
        db_name: str = None,
        partition_names: list = None
    ) -> list[dict | None]:
        url = self.base_url + "entities/get"
        payload = {
            "collectionName": collection_name,
            "id": ids,
            "outputFields": outputFields,
            "dbName": db_name,
            "partitionNames": partition_names
        }
        return await self.__post_execute(url, payload)

    async def query(
        self,
        collection_name: str,
        filter: str = None,
        limit: int = None,
        outputFields: list = None,
        offset: int = None,
        db_name: str = None,
        partition_names: list[str] = None
    ) -> list[dict | None]:
        # pylint: disable=redefined-builtin
        url = self.base_url + "entities/query"
        payload = {
            "collectionName": collection_name,
            "filter": filter,
            "limit": limit,
            "outputFields": outputFields,
            "offset": offset,
            "dbName": db_name,
            "partitionNames": partition_names
        }
        return await self.__post_execute(url, payload)

    async def upsert(
        self,
        collection_name: str,
        data: list[dict],
        db_name: str = None,
        partition_name: str = None
    ) -> dict:
        url = self.base_url + "entities/upsert"
        payload = {
            "collectionName": collection_name,
            "data": data,
            "dbName": db_name,
            "partitionName": partition_name
        }
        return await self.__post_execute(url, payload)

    async def insert(
        self,
        collection_name: str,
        data: list[dict],
        db_name: str = None,
        partition_name: str = None
    ) -> dict:
        url = self.base_url + "entities/insert"
        payload = {
            "collectionName": collection_name,
            "data": data,
            "dbName": db_name,
            "partitionName": partition_name
        }
        return await self.__post_execute(url, payload)

    async def delete(
        self,
        collection_name: str,
        filter: str,
        db_name: str = None,
        partition_name: str = None
    ) -> dict:
        url = self.base_url + "entities/delete"
        payload = {
            "collectionName": collection_name,
            "filter": filter,
            "dbName": db_name,
            "partitionName": partition_name
        }
        return await self.__post_execute(url, payload)
