from typing import Optional, List, Dict, Any
from typing_extensions import Literal
from .._models import BaseModel
from datetime import datetime


class ArtifactType(BaseModel):
    value: str


class ArtifactVersionInfo(BaseModel):
    author: str
    date_created: datetime
    description: Optional[str]
    name: str
    id: str
    uri: Optional[str]
    metadata: Dict[str, Any]


class Artifact(BaseModel):
    name: str
    author: str
    metadata: Dict[str, Any]
    artifact_type: ArtifactType
    date_created: datetime
    description: Optional[str]
    id: str
    is_public: bool
    pending_public_approval: bool
    latest_public_version_artifact: Optional[ArtifactVersionInfo]
    latest_registered_production_version_artifact: Optional[ArtifactVersionInfo]
    latest_registered_staging_version_artifact: Optional[ArtifactVersionInfo]
    latest_version_artifact: Optional[ArtifactVersionInfo]


class ArtifactCreated(BaseModel):
    id: str
    name: str
    author: str
    date_created: datetime
    description: Optional[str]
    is_public: bool
    pending_public_approval: bool
    metadata: Dict[str, Any]


class ArtifactCreateParams(BaseModel):
    name: str
    description: Optional[str]
    type: str
    metadata: Optional[Dict[str, Any]]
    is_public: bool = False
    author_level: Literal["user", "organization"] = "user"


class ArtifactUpdateReturn(BaseModel):
    id: str
    name: str


class ArtifactDeleteReturn(BaseModel):
    id: str
    name: str


class ArtifactUpdatedReturn(BaseModel):
    returning: List[ArtifactUpdateReturn]


class ArtifactUpdated(BaseModel):
    update_artifacts: ArtifactUpdatedReturn


class ArtifactUpdateParams(BaseModel):
    updates: Dict[str, Any]

    def __init__(self, **data):
        super().__init__(**data)
        self.updates = self.transform_updates()

    def transform_updates(self) -> str:
        return ",".join(f"{k}:{v}" for k, v in self.updates.items())


class ArtifactDeleted(BaseModel):
    returning: List[ArtifactDeleteReturn]


class ArtifactDownloadUrl(BaseModel):
    success: bool
    message: str
    files: List[Dict[str, str]]


class ArtifactUploadUrl(BaseModel):
    success: bool
    urls: List[Dict[str, str]]


class ArtifactQueryResult(BaseModel):
    artifacts: List[Artifact]
