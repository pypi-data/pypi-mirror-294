"""
This module provides the CLI for the Multiverse Platform SDK.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Union, Mapping, Callable

import httpx
from typing_extensions import Self, override

from almanak import resources, _exceptions
from almanak._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
)
from almanak._exceptions import AlmanakError, APIStatusError
from almanak._hasura import HasuraClient
from almanak._qs import Querystring
from ._streaming import Stream
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import (
    is_given,
    is_mapping,
)
from ._version import __version__

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "resources",
    "Almanak",
    "Client",
    "AlmanakClient",
    "AsyncAlmanak",
]
logger = logging.getLogger("almanak")
AlmanakUserMetadataProvider = Callable[[], "str | Awaitable[str]"]


def get_user_metadata(client: Almanak):
    """
    Retrieves the User Metadata from Almanak Platform if user metadata is not provided
    """

    try:
        response: httpx.Response = client.post("/auth/check-jwt", None)
        print(response.status_code)
        if response.status_code == 200:
            logger.debug("JWT is valid.")
            return response
        else:
            logger.warning(
                "Authentication failed with status code: {}".format(
                    response.status_code
                )
            )
            return None

    except Exception as e:
        logging.error("Error checking JWT", exc_info=True)
        raise ValueError(
            "Invalid token, please re-authenticate or get new token."
        ) from e


class Almanak(SyncAPIClient):
    """
    The Almanak class is a synchronous API client for the Multiverse Platform SDK.
    It provides access to various resources and configurations for the SDK.
    """

    library: resources.library
    # TODO, finish up the resources for these
    # data: resources.Data
    # deployment: resources.Deployment
    # optimization: resources.Optimization
    # price: resources.Price
    simulations: resources.Simulations
    users: resources.Users
    auth: resources.Auth

    # client options
    api_key: str
    organization: str | None
    team: str | None
    hasura_client: HasuraClient

    def __init__(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        team: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        almanak_user_metadata_provider: AlmanakUserMetadataProvider | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        _strict_response_validation: bool = False,
        _env="prod",  # Defaults to prod for end users
    ) -> None:
        """Construct a new synchronous almanak client instance.

        This automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` from `ALMANAK_API_KEY`
        - `organization` from `ALMANAK_ORG_ID`
        - `team` from `ALMANAK_TEAM_ID`
        """
        if api_key is None:
            api_key = os.environ.get("ALMANAK_API_KEY")  # type: ignore
        if api_key is None:
            raise AlmanakError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ALMANAK_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ALMANAK_BASE_URL")
        if base_url is None:
            if _env not in {"prod", "stage"}:
                raise ValueError("env can only be 'prod' or 'stage'")

            if _env == "stage":
                base_url = "https://api.stage.almanak.co"
            else:
                base_url = "https://api.almanak.co"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._hasura_client = HasuraClient(
            graph_api_url=self.graphql_url,
            rest_api_url=self.rest_url,
            platform_jwt=api_key,
        )

        # TODO: Get from Hasura

        if organization is None:
            organization = os.environ.get("ALMANAK_ORG_ID")
        self.organization = organization

        if team is None:
            team = os.environ.get("ALMANAK_TEAM_ID")
        self.team = team

        self._default_stream_cls = Stream

        self.library = resources.Library(self)
        self.simulations = resources.Simulations(self)
        self.auth = resources.Auth(self)
        # self.data = resources.Data(self)
        # self.deployment = resources.Deployment(self)
        # self.optimization = resources.Optimization(self)
        # self.price = resources.Price(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Almanak-Async": "false",
            "Almanak-Organization": (
                self.organization if self.organization is not None else Omit()
            ),
            "Almanak-Team": self.team if self.team is not None else Omit(),
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        organization: str | None = None,
        team: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError(
                "The `default_headers` and `set_default_headers` arguments are mutually exclusive"
            )

        if default_query is not None and set_default_query is not None:
            raise ValueError(
                "The `default_query` and `set_default_query` arguments are mutually exclusive"
            )

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            organization=organization or self.organization,
            team=team or self.team,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        data = body.get("error", body) if is_mapping(body) else body
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=data)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(
                err_msg, response=response, body=data
            )

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(
                err_msg, response=response, body=data
            )

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=data)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=data)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(
                err_msg, response=response, body=data
            )

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=data)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(
                err_msg, response=response, body=data
            )
        return APIStatusError(err_msg, response=response, body=data)


class AsyncAlmanak:
    # TODO
    pass


Client = Almanak  # Synonym for backwards compatibility
AlmanakClient = Almanak
AsyncClient = AsyncAlmanak
