import typing
import aioboto3.resources
from aioboto3.session import ResourceCreatorContext
from aiobotocore.config import AioConfig
from good_common.dependencies import BaseProvider, AsyncBaseProvider
import orjson
import jsonlines

# from s3transfer.manager import TransferConfig as S3TransferConfig
# from types_aiobotocore_s3.service_resource import TransferConfig
from boto3.s3.transfer import TransferConfig as S3TransferConfig
from fast_depends import inject, Depends
import aioboto3
import tqdm
import io
import os
from loguru import logger


def _provide_boto3(
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    aws_session_token: str | None = None,
    region_name: str | None = None,
    profile_name: str | None = None,
) -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name=region_name,
        profile_name=profile_name,
    )


class s3Client:
    @inject
    def __init__(
        self,
        session: aioboto3.Session = Depends(_provide_boto3),
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        region_name: str | None = None,
        profile_name: str | None = None,
        endpoint_url: str | None = None,
    ):
        self._session = session
        self._endpoint_url = endpoint_url

    # @property
    async def s3(self):
        print(self._endpoint_url)
        return await self._session.resource(
            "s3", endpoint_url=self._endpoint_url
        ).__aenter__()

    def bucket(self, name: str) -> "Bucket":
        return Bucket(name, client=self)


class Object:
    def __init__(
        self,
        obj: typing.Any,
        parent: typing.Any,
        key: str | None = None,
    ):
        self._obj = obj
        self.obj = None
        self.key = key or obj.key
        self.parent = parent
        self._data = None

    async def download(self, no_cache: bool = False) -> bytes:
        if not self._data or no_cache:
            self._data = await self.parent.download(self.key)
        return self._data

    async def data(self) -> bytes:
        if not self._data:
            return await self.download()
        return self._data

    async def read_lines(self, no_cache: bool = False, json: bool = False):
        data = await self.download(no_cache)
        if json:
            return jsonlines.Reader(io.BytesIO(data), _loads=orjson.loads)
        return io.BytesIO(data).readlines()

    async def json(self, no_cache: bool = False):
        return orjson.loads(await self.data())

    async def get(self, no_cache: bool = False):
        if not self.obj or no_cache:
            self.obj = await self._obj.get()
        return self.obj

    async def metadata(self):
        obj = await self.get()
        return await obj.get("Metadata")

    async def last_modified(self):
        obj = await self.get()
        return obj.get("LastModified")

    async def size(self):
        obj = await self.get()
        return obj.get("ContentLength")

    async def version_id(self):
        obj = await self.get()
        return obj.get("VersionId")

    async def content_type(self):
        obj = await self.get()
        return obj.get("ContentType")

    async def delete(self): ...

    def __repr__(self):
        return f"<Object s3://{self.parent.name}/{self.key}>"


class Bucket:
    @inject
    def __init__(
        self,
        bucket_name: str,
        client: s3Client = Depends(s3Client),
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        region_name: str | None = None,
        profile_name: str | None = None,
        endpoint_url: str | None = None,
    ):
        self.name = bucket_name
        self._client = client
        self._resource = None
        self._bucket = None

    @property
    def resource(self):
        if not self._resource:
            raise ValueError("Resource not initialized")
        return self._resource

    @property
    def bucket(self):
        if not self._bucket:
            raise ValueError("Bucket not initialized")
        return self._bucket

    @property
    def objects(self):
        if not self._bucket:
            raise ValueError("Bucket not initialized")
        return self._bucket.objects

    async def __aiter__(self):
        async for obj in self.objects.all():
            yield Object(obj=obj, parent=self.bucket)

    async def filter(self, prefix: str):
        async for obj in self.objects.filter(Prefix=prefix):
            yield Object(obj=obj, parent=self.bucket)

    async def items(self, prefix: str | None = None, list_versions: bool = False):
        async for obj in self.filter(prefix) if prefix else self:
            yield obj.key, Object(obj=obj, parent=self.bucket)

    async def __aenter__(self):
        self._resource = await self._client.s3()
        self._bucket = await self._resource.Bucket(self.name)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self._resource:
            await self._resource.__aexit__(exc_type, exc_value, traceback)
        self._resource = None
        self._bucket = None

    async def get(self, key: str):
        obj = await self.resource.ObjectSummary(self.name, key)
        return Object(obj=obj, parent=self.bucket)

    async def delete(self, key: str): ...

    async def download(
        self,
        key: str,
        config: S3TransferConfig | None = None,
        _size: int | None = None,
        progress: bool = False
    ):
        if not _size:
            obj = await self.resource.ObjectSummary(self.name, key)
            _size = await obj.size

        buffer = io.BytesIO()
        _progress = tqdm.tqdm(total=_size, unit="B", unit_scale=True, unit_divisor=1024, disable=not progress)

        def update_progress(x):
            _progress.n = x
            _progress.refresh()

        await self.bucket.download_fileobj(
            Key=key,
            Callback=update_progress,
            Fileobj=buffer,
            Config=config,
        )

        return buffer.getvalue()

    async def download_file(
        self,
        key: str,
        file: str,
        config: S3TransferConfig | None = None,
        progress: bool = False,
    ):
        obj = await self.get(key)
        _progress = tqdm.tqdm(total=await obj.size(), unit="B", unit_scale=True, unit_divisor=1024, disable=not progress)

        def update_progress(x):
            _progress.n = x
            _progress.refresh()

        await self.bucket.download_file(
            Key=key,
            Callback=update_progress,
            Filename=file,
            Config=config,
        )

        return file

    async def upload(
        self,
        key: str,
        data: bytes,
        content_type: str | None = None,
        metadata: dict | None = None,
        config: S3TransferConfig | None = None,
        progress: bool = False,
    ):
        buffer = io.BytesIO(data)

        _progress = tqdm.tqdm(desc=f"Uploading {key}", total=len(data), unit="B", unit_scale=True, unit_divisor=1024, disable=not progress)

        _extra_args: dict = {"ContentType": content_type or "application/octet-stream"}

        if metadata:
            _extra_args["Metadata"] = metadata

        await self.bucket.upload_fileobj(
            Key=key,
            Callback=_progress.update,
            Fileobj=buffer,
            ExtraArgs=_extra_args,
            Config=config,
        )

        return await self.get(key)

    async def upload_file(
        self,
        key: str,
        file: str,
        metadata: dict | None = None,
        config: S3TransferConfig | None = None,
        progress: bool = False,
    ):
        _size = os.path.getsize(file)
        _progress = tqdm.tqdm(desc=f"Uploading {key}", total=_size, unit="B", unit_scale=True, unit_divisor=1024, disable=not progress)

        _extra_args = {}

        if metadata:
            _extra_args["Metadata"] = metadata

        await self.bucket.upload_file(
            Filename=file,
            Key=key,
            Callback=_progress.update,
            ExtraArgs=_extra_args,
            Config=config,
        )

        return await self.get(key)

    def __repr__(self):
        return f"<Bucket {self.name}>"


class BucketProvider(BaseProvider[Bucket], Bucket):
    __env_access_key_id__: typing.ClassVar[str] = "AWS_ACCESS_TOKEN"
    __env_secret_key__: typing.ClassVar[str] = "AWS_SECRET_KEY"
    __env_endpoint_url__: typing.ClassVar[str] = "AWS_ENDPOINT_URL"

    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: str | None = None,
        aws_secret_access_key: str | None = None,
        aws_session_token: str | None = None,
        region_name: str | None = None,
        profile_name: str | None = None,
        endpoint_url: str | None = None,
    ):
        super().__init__(
            bucket_name=bucket_name,
            aws_access_key_id=aws_access_key_id
            or os.environ.get(self.__env_access_key_id__),
            aws_secret_access_key=aws_secret_access_key
            or os.environ.get(self.__env_secret_key__),
            aws_session_token=aws_session_token,
            region_name=region_name,
            profile_name=profile_name,
            endpoint_url=endpoint_url or os.environ.get(self.__env_endpoint_url__),
        )

    def initializer(
        self,
        cls_args: typing.Tuple[typing.Any],
        cls_kwargs: typing.Dict[str, typing.Any],
        fn_kwargs: typing.Dict[str, typing.Any],
    ):
        cls_kwargs.update(fn_kwargs)
        return cls_args, cls_kwargs
