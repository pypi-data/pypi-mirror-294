from typing import cast

ExcMeta: type = type(Exception)


class BaseException(Exception):
    message: str | None = None

    def __init__(self, *args: object, **kwargs: object) -> None:
        try:
            (message, *extra_args) = args
            if isinstance(message, str):
                self.message = message
        except ValueError:
            pass

        for key, val in kwargs.items():
            setattr(self, key, val)


class ProgrammingError(BaseException):
    pass


class ServiceExceptionMeta(ExcMeta):
    registry: dict[str, type] = {}
    generic_registry: dict[int, type] = {}

    def __new__(cls, name, bases, namespace, **kwargs):
        """Saves every `ServiceException` subclass to an internal registry keyed
        by class name. If `http_generic` is set to `True`, it will additionally be saved to
        the generic status code registry."""
        if name in cls.registry:
            raise ProgrammingError("Duplicate exception name in registry.")
        generic = namespace.get("http_generic", False)
        # do not include inherit http_generic in actual class
        # so it is never inherited
        namespace["http_generic"] = False

        exc_cls = super().__new__(cls, name, bases, namespace, **kwargs)
        cls.registry[name] = exc_cls
        status_code = namespace.get("http_status_code")
        if generic and (status_code is not None):
            if status_code in cls.generic_registry:
                raise ProgrammingError("Duplicate status code in generic registry.")

            cls.generic_registry[status_code] = exc_cls
        return exc_cls

    @classmethod
    def get_exception_class(cls, name: str) -> type["ServiceException"] | None:
        return cls.registry.get(name)

    @classmethod
    def get_generic_exception_class(cls, status_code: int):
        return cls.generic_registry.get(status_code)


class ServiceException(BaseException, metaclass=ServiceExceptionMeta):
    http_status_code: int = 500
    http_error_name: str = "service_exception"

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        kwargs.setdefault("http_status_code", self.http_status_code)
        kwargs.setdefault("http_error_name", self.http_error_name)
        super().__init__(
            *args,
            **kwargs,
        )
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def from_status_code(cls, status_code: int) -> "ServiceException":
        exc_class = ServiceExceptionMeta.get_generic_exception_class(status_code)

        if exc_class is None:
            raise ValueError(
                f"No generic exception available for status code {str(status_code)}."
            )
        return exc_class()

    @classmethod
    def from_dict(cls, dict_: dict) -> "ServiceException":
        name = dict_.get("name", "__dne__")
        exc_class = ServiceExceptionMeta.get_exception_class(name)

        if exc_class is None:
            raise ValueError(f"'{name}' does not exist in exception registry.")

        args = cast(tuple, dict_.get("args"))
        kwargs = cast(dict, dict_.get("kwargs"))
        return exc_class(*args, **kwargs)

    def to_dict(self):
        return {
            "args": self.args,
            "kwargs": self.kwargs,
            "name": self.__class__.__name__,
        }


class ServerError(ServiceException):
    message = "An unknown server error occurred."
    http_status_code = 500
    http_error_name = "server_error"
    http_generic = True


class BadGateway(ServiceException):
    message = "Bad Gateway"
    http_status_code = 502
    http_error_name = "bad_gateway"
    http_generic = True


class ServiceUnavailable(ServiceException):
    message = "Service Unavailable"
    http_status_code = 503
    http_error_name = "service_unavailable"
    http_generic = True


class Unauthorized(ServiceException):
    message = "Unauthorized"
    http_status_code = 401
    http_error_name = "unauthorized"
    http_generic = True


class Forbidden(ServiceException):
    message = "Authentication credentials indicate insufficient permissions."
    http_status_code = 403
    http_error_name = "forbidden"
    http_generic = True


class NotFound(ServiceException):
    message = "Not Found"
    http_status_code = 404
    http_error_name = "not_found"
    http_generic = True


class InvalidToken(Unauthorized):
    message = "The supplied token is invalid."
    http_status_code = 401
    http_error_name = "invalid_token"


class InvalidCredentials(Unauthorized):
    message = "Authentication credentials rejected."
    http_status_code = 401
    http_error_name = "invalid_credentials"
