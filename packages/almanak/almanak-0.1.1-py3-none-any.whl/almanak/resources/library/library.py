from __future__ import annotations

from .artifacts import Artifacts
from ..._compat import cached_property
from ..._resource import SyncAPIResource

from ..._base_client import make_request_options
from ..._resource import SyncAPIResource
from ...types.artifact import ArtifactDeleted


__all__ = ["Library"]


class Library(SyncAPIResource):
    @cached_property
    def artifacts(self) -> Artifacts:
        return Artifacts(self._client)

    def delete_file(self, file_id: str, **kwargs) -> ArtifactDeleted:
        return self._delete(
            "/library/delete_artifact_file_by_id",
            body={"fileId": file_id},
            options=make_request_options(**kwargs),
            cast_to=ArtifactDeleted,
        )
