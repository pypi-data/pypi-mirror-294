from __future__ import annotations

from typing import Optional, List

from almanak._base_client import make_request_options
from almanak._resource import SyncAPIResource
from almanak._utils import maybe_transform
from almanak.types.artifact_version import (
    ArtifactVersion,
    ArtifactVersionUpdated,
    ArtifactVersionUpdateParams,
    ArtifactDownloadUrl,
    ArtifactUploadUrl,
)
from almanak.types.artifact import ArtifactDeleteReturn
from almanak.pagination import SyncPage

__all__ = ["Versions"]


class Versions(SyncAPIResource):
    def list(
        self, artifact_name: str, *, limit: int = 100, offset: int = 0, **kwargs
    ) -> SyncPage[ArtifactVersion]:
        return self._get_api_list(
            f"/library/artifacts/{artifact_name}/versions",
            page=SyncPage[ArtifactVersion],
            options=make_request_options(**kwargs),
            model=ArtifactVersion,
            body={"limit": limit, "offset": offset},
        )

    def retrieve(self, artifact_name: str, version: str, **kwargs) -> ArtifactVersion:
        return self._get(
            f"/library/artifacts/{artifact_name}/versions/{version}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersion,
        )

    def download(
        self, artifact_name: str, version: str, **kwargs
    ) -> ArtifactDownloadUrl:
        return self._get(
            f"/library/artifacts/{artifact_name}/versions/{version}/url",
            options=make_request_options(**kwargs),
            cast_to=ArtifactDownloadUrl,
        )

    def get_uris(self, artifact_name: str, version: str, **kwargs) -> List[str]:
        return self._get(
            f"/library/artifacts/{artifact_name}/versions/{version}/uri",
            options=make_request_options(**kwargs),
            cast_to=List[str],
        )

    def upload(
        self, artifact_name: str, version: str, files: List[str], **kwargs
    ) -> ArtifactUploadUrl:
        return self._post(
            f"/library/artifacts/{artifact_name}/versions/{version}/upload",
            body={"files": files},
            options=make_request_options(**kwargs),
            cast_to=ArtifactUploadUrl,
        )

    def update(
        self,
        artifact_name: str,
        version: str,
        *,
        updates: dict,
        **kwargs,
    ) -> ArtifactVersionUpdated:
        body = {
            "updates": updates,
        }
        return self._post(
            f"/library/artifacts/{artifact_name}/versions/{version}",
            body=maybe_transform(body, ArtifactVersionUpdateParams),
            options=make_request_options(**kwargs),
            cast_to=ArtifactVersionUpdated,
        )

    def delete(
        self, artifact_name: str, version: str, **kwargs
    ) -> ArtifactDeleteReturn:
        return self._delete(
            f"/library/artifacts/{artifact_name}/versions/{version}",
            options=make_request_options(**kwargs),
            cast_to=ArtifactDeleteReturn,
        )
