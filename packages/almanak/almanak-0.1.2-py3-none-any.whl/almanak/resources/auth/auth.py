from __future__ import annotations

from .api_keys import ApiKeys
from ..._compat import cached_property
from ..._resource import SyncAPIResource

__all__ = ["Auth"]


class Auth(SyncAPIResource):
    @cached_property
    def api_keys(self) -> ApiKeys:
        return ApiKeys(self._client)
