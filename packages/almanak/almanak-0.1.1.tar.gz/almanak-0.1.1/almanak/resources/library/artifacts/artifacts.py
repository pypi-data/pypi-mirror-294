from __future__ import annotations

from typing import Optional, List


from almanak._base_client import make_request_options
from almanak._resource import SyncAPIResource
from almanak._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from almanak._utils import maybe_transform
from almanak.pagination import SyncPage
from almanak.types.artifact import (
    ArtifactQueryResult,
    ArtifactCreated,
    ArtifactCreateParams,
    ArtifactUpdated,
    ArtifactUpdateParams,
    ArtifactDeleted,
    Artifact,
)
from almanak.types.artifact_version import ArtifactVersion, ArtifactVersionUploaded
import json

from .versions import Versions

__all__ = ["Artifacts"]


class Artifacts(SyncAPIResource):
    @property
    def versions(self) -> Versions:
        return Versions(self._client)

    def create(
        self,
        *,
        artifact_name: str,
        description: Optional[str] = None,
        type: str,
        metadata: Optional[dict] = None,
        is_public: bool = False,
        author_level: str = "user",
    ) -> ArtifactCreated:
        body = {
            "name": artifact_name,
            "description": description,
            "type": type,
            "metadata": metadata,
            "is_public": is_public,
            "author_level": author_level,
        }
        return self._post(
            "library/artifacts",
            body=maybe_transform(body, ArtifactCreateParams),
            options=make_request_options(),
            cast_to=ArtifactCreated,
        )

    def retrieve(self, artifact_name: str, **kwargs) -> ArtifactQueryResult:
        return self._get(
            f"/library/artifacts/{artifact_name}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactQueryResult,
        )

    def retrieve_latest(self, artifact_name: str, **kwargs) -> ArtifactVersion:
        return self._get(
            f"/library/artifacts/{artifact_name}/latest",
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersion,
        )

    def upload_new_version(
        self, artifact_name: str, files: List[str], **kwargs
    ) -> ArtifactVersionUploaded:
        return self._post(
            f"/library/artifacts/{artifact_name}/version/upload-urls",
            body={"files": files},
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersionUploaded,
        )

    def list(
        self, *, limit: int = 100, offset: int = 0, **kwargs
    ) -> SyncPage[Artifact]:
        return self._get_api_list(
            "/library/artifacts/",
            page=SyncPage[Artifact],
            options=make_request_options(**kwargs),
            model=Artifact,
            body={"limit": limit, "offset": offset},
        )

    def delete(self, artifact_name: str, **kwargs) -> ArtifactDeleted:
        return self._delete(
            f"/library/artifacts/{artifact_name}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactDeleted,
        )

    def update(
        self,
        artifact_name: str,
        *,
        updates: dict,
        **kwargs,
    ) -> ArtifactUpdated:

        body = {"updates": updates}
        return self._post(
            f"/library/artifacts/{artifact_name}",
            body=maybe_transform(body, ArtifactUpdateParams),
            options=make_request_options(**kwargs),
            cast_to=ArtifactUpdated,
        )
