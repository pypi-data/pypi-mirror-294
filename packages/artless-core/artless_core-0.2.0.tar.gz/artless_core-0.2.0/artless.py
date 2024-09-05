"""The artless and minimalistic web library for creating small applications or APIs."""

__author__ = "Peter Bro"
__version__ = "0.2.0"
__license__ = "MIT"
__all__ = ["App", "Config", "Request", "Response", "ResponseFactory"]

from copy import deepcopy
from datetime import datetime
from http import HTTPStatus
from logging import Logger
from logging import config as logging_config
from logging import getLogger
from re import Pattern, compile, match
from time import time
from traceback import format_exc
from typing import (
    Any,
    Callable,
    ClassVar,
    Mapping,
    MutableMapping,
    Optional,
    ParamSpec,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
    runtime_checkable,
)
from urllib.parse import SplitResult, parse_qs, quote, urlsplit
from uuid import UUID, uuid4

# Prioritized import of josn library: orjson || ujson || cjson || json (standart module)
try:
    from orjson import JSONEncoder, loads
except ImportError:
    try:
        from json import JSONEncoder

        from ujson import loads
    except ImportError:
        try:
            from cjson import JSONEncoder, loads
        except ImportError:
            from json import JSONEncoder, loads

# Types
T = TypeVar("T")
P = ParamSpec("P")
RF = TypeVar("RF", bound="ResponseFactory")

CommonDictT = dict[str, Any]
CommonDataT = Mapping | Sequence[T] | str | int | float | bool | datetime | None

EnvironT = Mapping[str, Any]
WSGIRetvalT = TypeVar("WSGIRetvalT", covariant=True)
StartResponseT = Callable[[str, Sequence[tuple[str, str]]], str]

RouteT = tuple[str, str, Callable]
HandlerT = Callable[["Request"], "Response"]
RoutingTableT = MutableMapping[str, MutableMapping[Pattern, HandlerT]]

# Constants and defaults
HTTP_PREFIX: str = "HTTP_"
UNPREFIXED_HEADERS: frozenset[str] = frozenset(["CONTENT_TYPE", "CONTENT_LENGTH"])
CTYPE_HEADER_NAME: str = "Content-Type"
DEFAULT_CTYPE: str = "text/plain"
DEFAULT_CONFIG: CommonDictT = {
    "debug": False,
    "logging": {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[{asctime}] [{process:d}] [{levelname}] {message}",
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "style": "{",
            },
        },
        "handlers": {
            "stdout": {
                "formatter": "default",
                "level": "INFO",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "artless": {
                "level": "INFO",
                "handlers": ["stdout"],
                "propagate": False,
            }
        },
        "root": {"level": "WARNING", "handlers": ["stdout"]},
    },
}


@runtime_checkable
class BodyDecoder(Protocol):
    def decode(self, body: bytes) -> Mapping[str, CommonDataT]: ...


@runtime_checkable
class WSGIProtocol(Protocol[WSGIRetvalT]):
    def __call__(self, environ: EnvironT, start_response: StartResponseT) -> Sequence[bytes]: ...


class Config:
    __config: CommonDictT
    _instance: ClassVar[Optional["Config"]] = None

    def __new__(cls: Type["Config"]):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__config = deepcopy(DEFAULT_CONFIG)
        return cls._instance

    def __getattr__(self, name: str) -> Any:
        return self.__config[name]

    @property
    def current(self) -> CommonDictT:
        return self.__config

    def replace(self, params: CommonDictT) -> None:
        self.__config |= params


logging_config.dictConfig(Config().logging)
logger: Logger = getLogger(__name__)


def encode_json(data: CommonDataT, encoder: Type[JSONEncoder] = JSONEncoder) -> str:
    return encoder().encode(data)


class WSGIHeadersParser:
    __slots__ = ("headers",)

    def __init__(self, environ: EnvironT) -> None:
        self.headers: Mapping[str, str] = {}

        for header, value in environ.items():
            if name := self._transcribe_header_name(header):
                self.headers[name] = value

    def _transcribe_header_name(self, header: str) -> Optional[str]:
        if header.startswith(HTTP_PREFIX):
            # NOTE: hardcoded constant length instead of calculating len(HTTP_PREFIX)
            header = header[5:]
        elif header not in UNPREFIXED_HEADERS:
            return None
        return header.replace("_", "-").title()


class JSONBodyDecoder(BodyDecoder):
    def decode(self, body: bytes) -> Mapping[str, CommonDataT]:
        return loads(body)


class WWWFormBodyDecoder(BodyDecoder):
    def decode(self, body: bytes) -> Mapping[str, CommonDataT]:
        result: CommonDictT = {}
        for param, value in parse_qs(body.decode()).items():
            result[param] = value if len(value) > 1 else value[0]
        return result


CTYPE_DECODERS: Mapping[str, Type[BodyDecoder]] = {
    "application/json": JSONBodyDecoder,
    "application/x-www-form-urlencoded": WWWFormBodyDecoder,
}


class Request:
    __slots__ = ("_raw_input", "_splitted_url", "headers", "id", "method", "params", "url")

    def __init__(self, environ: EnvironT) -> None:
        self.id: UUID = uuid4()

        script_url: str = environ.get("SCRIPT_URL", "").rstrip("/")
        path_info: str = environ.get("PATH_INFO", "/").replace("/", "", 1)
        content_length: int = int(environ.get("CONTENT_LENGTH") or "0")
        query_string: Optional[str] = environ.get("QUERY_STRING")

        self.url: str = f"{script_url}/{path_info}"
        if query_string:
            self.url += f"?{query_string}"

        self._splitted_url: SplitResult = urlsplit(self.url)
        self._raw_input: bytes = environ["wsgi.input"].read(content_length)

        self.method: str = environ["REQUEST_METHOD"].upper()
        self.headers: Mapping[str, str] = WSGIHeadersParser(environ).headers

        # Unpack single values ​​for simplicity
        self.params: CommonDictT = {
            param: (values[0] if len(values) == 1 else values)
            for param, values in parse_qs(self._splitted_url.query).items()
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.method} {self.url}>"

    @property
    def path(self) -> str:
        return self._splitted_url.path

    @property
    def query(self) -> str:
        return self._splitted_url.query

    @property
    def fragment(self) -> str:
        return self._splitted_url.fragment

    @property
    def content_type(self) -> Optional[str]:
        return self.headers.get("Content-Type")

    @property
    def user_agent(self) -> Optional[str]:
        return self.headers.get("User-Agent")

    @property
    def body(self) -> Mapping[str, CommonDataT] | bytes:
        if not self.content_type:
            return self._raw_input
        # NOTE: .partition is slightly faster than .split
        ctype = self.content_type.partition(";")[0]
        if decoder := self._get_body_decoder(ctype):
            return decoder().decode(self._raw_input)
        return self._raw_input

    @staticmethod
    def _get_body_decoder(ctype: str) -> Optional[Type[BodyDecoder]]:
        if ctype in CTYPE_DECODERS:
            return CTYPE_DECODERS[ctype]
        return None


class Response:
    __slots__ = ("_body", "_status", "headers")

    def __init__(self, *, status: HTTPStatus = HTTPStatus.OK) -> None:
        self._body: bytes = b""
        self._status: HTTPStatus = status
        self.headers: MutableMapping[str, str] = {CTYPE_HEADER_NAME: DEFAULT_CTYPE}

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.status}>"

    @property
    def status(self) -> str:
        return f"{self._status.value} {self._status.phrase}"

    @status.setter
    def status(self, status: HTTPStatus) -> None:
        self._status = status

    @property
    def content_type(self) -> str:
        return self.headers[CTYPE_HEADER_NAME]

    @content_type.setter
    def content_type(self, value: str) -> None:
        self.headers[CTYPE_HEADER_NAME] = value

    @property
    def body(self) -> bytes:
        return self._body

    @body.setter
    def body(self, data: Union[str, bytes]) -> None:
        if isinstance(data, str):
            self._body = (data + "\n").encode("utf-8")
        elif isinstance(data, bytes):
            data += b"\n"
            self._body = data
        else:
            raise TypeError(f"Response body must be only string or bytes, not {type(data)}")
        self.headers["Content-Length"] = str(len(self._body))

    def _dump_headers(self) -> Sequence[tuple[str, str]]:
        return [(name, value) for name, value in self.headers.items()]


class ResponseFactory:
    __slots__: set[str] = set()

    @classmethod
    def create(cls: Type[RF], /, *, status: HTTPStatus = HTTPStatus.OK) -> Response:
        response = Response()
        response.status = status  # type: ignore[assignment]
        return response

    @classmethod
    def plain(cls: Type[RF], message: str, /, *, status: HTTPStatus = HTTPStatus.OK) -> Response:
        response = Response(status=status)
        response.body = message  # type: ignore[assignment]
        return response

    @classmethod
    def html(cls: Type[RF], template: str, /, *, status: HTTPStatus = HTTPStatus.OK) -> Response:
        response = Response(status=status)
        response.content_type = "text/html"
        response.body = template  # type: ignore[assignment]
        return response

    @classmethod
    def json(
        cls: Type[RF], data: CommonDataT, /, *, status: HTTPStatus = HTTPStatus.OK
    ) -> Response:
        response = Response(status=status)
        response.content_type = "application/json"
        response.body = encode_json(data)  # type: ignore[assignment]
        return response

    @classmethod
    def redirect(
        cls: Type[RF], url: str, /, *, status: HTTPStatus = HTTPStatus.MOVED_PERMANENTLY
    ) -> Response:
        response = Response(status=status)
        response.headers["Location"] = quote(url)
        del response.headers[CTYPE_HEADER_NAME]
        return response


class App(WSGIProtocol):
    __slots__ = ("_id", "_routing_table", "_start_response", "_start_time")

    def __init__(self) -> None:
        self._routing_table: RoutingTableT = {}

    def __call__(self, environ: EnvironT, start_response: StartResponseT):
        self._start_time: float = time()
        self._start_response: StartResponseT = start_response

        request = Request(environ)
        method, path = (request.method, request.path)

        if method not in self._routing_table:
            return self._wsgi_response(request, Response(status=HTTPStatus.METHOD_NOT_ALLOWED))

        handler, params = (None, None)
        for pattern, _handler in self._routing_table[method].items():
            if match_result := match(pattern, path):
                handler, params = (_handler, match_result.groupdict())

        if not handler:
            return self._wsgi_response(request, Response(status=HTTPStatus.NOT_FOUND))

        try:
            response = handler(request, **params)
        except Exception:
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            stack_trace = format_exc()
            if Config().debug:
                response.body = stack_trace  # type: ignore[assignment]
            logger.error(f"[{request.id}] {stack_trace}")

        return self._wsgi_response(request, response)

    def add_route(self, route: RouteT) -> None:
        method, path, handler = route
        method = method.upper()
        compiled_re_path: Pattern = compile(path)
        if method not in self._routing_table:
            self._routing_table[method] = {}
        if compiled_re_path in self._routing_table[method]:
            raise ValueError(f'Route for "{method} {path}" already exists!')
        self._routing_table[method][compiled_re_path] = handler

    def set_routes(self, routes: Sequence[RouteT]) -> None:
        for route in routes:
            self.add_route(route)

    def _wsgi_response(self, request: Request, response: Response) -> Sequence[bytes]:
        logger.info(
            f"[{request.id}] {request.method} {request.path} "
            f"{response.status} in {(time() - self._start_time) * 1000:.3f}ms."
        )
        self._start_response(response.status, response._dump_headers())
        return [response.body]
