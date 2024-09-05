import logging
from json.decoder import JSONDecodeError

import httpx

from toolkit.exceptions import ServerError, ServiceException

logger = logging.getLogger(__name__)


class ServiceClient(object):
    url: str
    auth: httpx.Auth | None
    http_client: httpx.Client

    def __init__(
        self,
        url: str,
        auth: httpx.Auth | None = None,
        timeout: int = 10,
    ) -> None:
        self.url = url
        self.auth = auth
        logger.debug(f"Making new http service client for url={url} auth={auth}.")
        self.http_client = httpx.Client(
            base_url=self.url,
            timeout=timeout,
            http2=True,
            auth=auth,
        )

    def raise_code_or_unknown(self, name: str | None, res: httpx.Response):
        try:
            raise ServiceException.from_status_code(res.status_code)
        except ValueError:
            raise ServerError(http_error_name=name, http_status_code=res.status_code)

    def raise_dict_or_unknown(self, dict_: dict, res: httpx.Response):
        try:
            raise ServiceException.from_dict(dict_)
        except ValueError:
            self.raise_code_or_unknown(dict_.get("name"), res)

    def raise_service_exception(self, res: httpx.Response):
        if res.is_error:
            try:
                json = res.json()
            except (ValueError, JSONDecodeError):
                self.raise_code_or_unknown(res.text, res)

            self.raise_dict_or_unknown(json, res)
