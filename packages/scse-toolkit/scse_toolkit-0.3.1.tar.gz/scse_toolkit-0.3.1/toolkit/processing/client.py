import logging
from typing import TypeVar

import httpx
from pydantic import BaseModel

from ..client import ServiceClient
from .models import Root, Task

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=BaseModel)


class ProcessingClient(ServiceClient):
    def __init__(
        self, url: str, auth: httpx.Auth | None = None, timeout: int = 10
    ) -> None:
        logger.debug(
            f"Connecting to scse-processing instance at '{url}' using "
            f"auth class `{auth}`..."
        )
        super().__init__(url, auth=auth, timeout=timeout)
        self.check_root()

    def check_root(self):
        """Requests root api endpoint."""
        res = self.http_client.get("/")
        self.raise_service_exception(res)
        root = Root(**res.json())
        return root

    def start_basic_task(self) -> Task:
        res = self.http_client.post("tasks/basic")
        self.raise_service_exception(res)
        return Task(**res.json())

    def start_sleep_task(self, seconds: int = 1) -> Task:
        res = self.http_client.post("tasks/sleep", json={"seconds": seconds})
        self.raise_service_exception(res)
        return Task(**res.json())

    def retrieve_task(self, id: str) -> Task:
        res = self.http_client.get(f"tasks/{id}/")
        self.raise_service_exception(res)
        return Task(**res.json())
