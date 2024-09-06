import json
import logging
from collections.abc import Iterable
from typing import Generic, TypeVar

import httpx
from pydantic import BaseModel

from ..client import ServiceClient
from .models import Ixmp4Instance, Root, User

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)


class ModelRepository(Generic[ModelType]):
    response_model: type[ModelType]
    prefix: str
    client: ServiceClient

    def __init__(
        self, client: ServiceClient, prefix: str, response_model: type[ModelType]
    ) -> None:
        self.client = client
        self.prefix = prefix
        self.response_model = response_model

        if not self.prefix.endswith("/"):
            self.prefix += "/"

    def normalize_params(self, params: dict) -> dict[str, str]:
        """Encodes list parameters as comma-seperated strings because
        httpx does not have a way to customize this behaviour."""

        for key, val in params.items():
            if isinstance(val, Iterable) and not isinstance(val, str):
                list_ = list(json.dumps(i) for i in val)
                params[key] = ",".join(list_)
        return params

    def list(self, **kwargs) -> list[ModelType]:
        """Retrieves a list of objects."""
        logger.debug(f"Listing `{self.response_model.__name__}` objects...")
        res = self.client.http_client.get(
            self.prefix,
            params=self.normalize_params({"page_size": -1, **kwargs}),
        )
        self.client.raise_service_exception(res)
        json = res.json()
        return [self.response_model(**r) for r in json.get("results", [])]

    def retrieve(self, id: int) -> ModelType:
        """Retrieves an object with the supplied id."""
        logger.debug(f"Retrieving `{self.response_model.__name__}` object...")
        res = self.client.http_client.get(self.prefix + str(id) + "/")
        self.client.raise_service_exception(res)
        return self.response_model(**res.json())


class UserRepository(ModelRepository[User]):
    def __init__(self, client: ServiceClient) -> None:
        super().__init__(client, "users/", User)

    def impersonate(self, id: int) -> dict[str, str]:
        """Retrieves new authentication tokens for the
        user with the supplied id. Only works if
        a `superuser` authentication token is set."""

        res = self.client.http_client.get(self.prefix + str(id) + "/impersonate/")
        self.client.raise_service_exception(res)
        return res.json()

    def me(self):
        """Retrieves the current user if an authentication
        token is set."""

        res = self.client.http_client.get(self.prefix + "me/")
        self.client.raise_service_exception(res)
        return self.response_model(**res.json())


class ManagerClient(ServiceClient):
    def __init__(
        self, url: str, auth: httpx.Auth | None = None, timeout: int = 10
    ) -> None:
        logger.debug(
            f"Connecting to manager instance at '{url}' using "
            f"auth class `{auth}`..."
        )
        super().__init__(url, auth=auth, timeout=timeout)

        self.check_root()

        self.ixmp4 = ModelRepository(self, "ixmp4/", Ixmp4Instance)
        self.users = UserRepository(self)

    def check_root(self):
        """Requests root api endpoint and logs messages."""
        res = self.http_client.get("/")
        self.raise_service_exception(res)
        root = Root(**res.json())

        for warning in root.messages.get("warning", []):
            logger.warn(warning)

        for info in root.messages.get("info", []):
            logger.info(info)
