from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr

from .urls import DatasetUrl

# Note that instance types above 4xlarge are undocumented publicly
WHITELISTED_INSTANCE_TYPES = Literal[
    "m5.large",
    "m5.xlarge",
    "m5.2xlarge",
    "m5.4xlarge",
    "m5.8xlarge",
    "m5.12xlarge",
    "m5.16xlarge",
    "r5.large",
    "r5.xlarge",
    "r5.2xlarge",
    "r5.4xlarge",
    "r5.8xlarge",
    "r5.12xlarge",
    "r5.16xlarge",
]


class SampleMapRequest(BaseModel):
    file_id: Optional[str] = None
    chunk_id: Optional[int] = None
    n_rows: Optional[int] = None
    model_config = ConfigDict(populate_by_name=True)


class WholeFileSampleMapRequest(BaseModel):
    file_id: str = None
    n_rows: Optional[int] = None
    model_config = ConfigDict(populate_by_name=True)


class GetTableBboxRequest(BaseModel):
    path: str
    bbox_minx: float
    bbox_miny: float
    bbox_maxx: float
    bbox_maxy: float

    n_rows: Optional[int] = None
    clip: bool = True
    columns: Optional[List[str]] = None
    buffer: Optional[float] = None
    model_config = ConfigDict(populate_by_name=True)


class SampleJoinRequest(BaseModel):
    file_id: Optional[str] = None
    chunk_id: Optional[int] = None
    n_rows: Optional[int] = None
    model_config = ConfigDict(populate_by_name=True)


class SampleSingleFileJoinRequest(BaseModel):
    file_id: Optional[str] = None
    chunk_id: Optional[int] = None
    n_rows: Optional[int] = None
    model_config = ConfigDict(populate_by_name=True)


class StartJobRequest(BaseModel):
    region: Optional[StrictStr] = None
    instance_type: Optional[WHITELISTED_INSTANCE_TYPES] = None
    disk_size_gb: Optional[StrictInt] = None
    additional_env: Optional[List[StrictStr]] = Field(default_factory=list)
    backend: Optional[StrictStr] = None


class ListJobsRequest(BaseModel):
    skip: Optional[StrictInt] = None
    limit: Optional[StrictInt] = None


class SaveUdfRequest(BaseModel):
    slug: Optional[str] = None
    udf_body: str
    allow_public_read: Optional[bool] = None
    allow_public_list: Optional[bool] = None


class ListUdfsRequest(BaseModel):
    skip: Optional[StrictInt] = None
    limit: Optional[StrictInt] = None


class GetPathRequest(BaseModel):
    path: DatasetUrl


class SignPathRequest(BaseModel):
    path: DatasetUrl


class ListPathRequest(BaseModel):
    path: DatasetUrl


class DeletePathRequest(BaseModel):
    path: DatasetUrl
    max_deletion_depth: Union[Optional[int], Literal["unlimited"]]


class ResolvePathRequest(BaseModel):
    path: DatasetUrl


class UploadRequest(BaseModel):
    path: DatasetUrl


class UploadTempRequest(BaseModel):
    extension: Optional[str] = None


class ListUdfAccessTokensRequest(BaseModel):
    skip: Optional[StrictInt] = None
    limit: Optional[StrictInt] = None


class CreateUdfAccessTokenRequest(BaseModel):
    udf_email: Optional[str] = None
    udf_slug: Optional[str] = None
    udf_id: Optional[str] = None
    client_id: Optional[str] = None
    cache: bool = True
    metadata_json: Dict[str, Any] = {}
    enabled: bool = True


class UpdateUdfAccessTokenRequest(BaseModel):
    client_id: Optional[str] = None
    cache: Optional[bool] = None
    metadata_json: Optional[Dict[str, Any]] = None
    enabled: Optional[bool] = None
