from typing import Optional, List, Dict, Any
from .._models import BaseModel
from datetime import datetime


class ArtifactVersion(BaseModel):
    name: str
    id: str
    description: Optional[str]
    date_created: datetime
    metadata: Dict[str, Any]
    author: str
    is_public: bool
    artifact: Dict[str, str]


class ArtifactVersionWithType(BaseModel):
    name: str
    author: str
    date_created: datetime
    description: Optional[str]
    is_public: bool
    metadata: Dict[str, Any]
    artifact: Dict[str, str]


class ArtifactVersionQueryResult(BaseModel):
    versions: List[ArtifactVersionWithType]


class ArtifactVersionInfo(BaseModel):
    author: str
    date_created: datetime
    description: Optional[str]
    name: str
    id: str
    uri: Optional[str]
    metadata: Dict[str, Any]


class ArtifactVersionArtifactReturn(BaseModel):
    name: str


class ArtifactVersionUpdateReturn(BaseModel):
    id: str
    artifact: List[ArtifactVersionArtifactReturn]
    name: str


class ArtifactVersionUpdated(BaseModel):
    update_artifacts: List[ArtifactVersionUpdateReturn]


class ArtifactUpdatedReturn(BaseModel):
    returning: List[ArtifactVersionUpdateReturn]


class ArtifactVersionUpdateParams(BaseModel):
    updates: Dict[str, Any]

    def __init__(self, **data):
        super().__init__(**data)
        self.updates = self.transform_updates()

    def transform_updates(self) -> str:
        return ",".join(f"{k}:{v}" for k, v in self.updates.items())


class ArtifactVersionUploaded(BaseModel):
    success: bool
    message: str
    version: str
    urls: List[Dict[str, str]]


class ArtifactDownloadUrl(BaseModel):
    success: bool
    message: str
    files: List[Dict[str, str]]


class ArtifactUploadUrl(BaseModel):
    success: bool
    urls: List[Dict[str, str]]
