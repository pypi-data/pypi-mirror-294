# artless-core

![PyPI - License](https://img.shields.io/pypi/l/artless-core)
![PyPI Version](https://img.shields.io/pypi/v/artless-core)
![Development Status](https://img.shields.io/badge/development%20status-3%20--%20Alpha-orange)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/artless-core)
[![Downloads](https://static.pepy.tech/badge/artless-core)](https://pepy.tech/project/artless-core)

The artless and minimalistic web library for creating small applications or APIs.

## Motivation

An extremely minimalistic framework was needed to create the same minimalistic applications. Those "micro" frameworks like `Flask`, `Pyramid`, `CherryPie`, etc - turned out to be not micro at all). Even a single-module `Bottle` turned out to be a "monster" of 4 thousand LOC and supporting compatibility with version 2.7.

Therefore, it was decided to sketch out our own simple, minimally necessary implementation of the WSGI library for creating small/simple web app.

## Main principles

1. Artless, fast and small (less then 400 LOC) single-file module.
2. No third party dependencies (standart library only).
3. Support only modern versions of Python (>=3.10).
4. Mostly pure functions without side effects.
5. Interfaces with type annotations.
6. Comprehensive documentation with examples of use.
7. Full test coverage.

## Limitations

* No `Async/ASGI` support.
* No `WebSocket` support.
* No `Cookies` support.
* No `multipart/form-data` support.
* No built-in protections, such as: `CSRF`, `XSS`, `clickjacking` and other.

## Installation

``` shellsession
$ pip install artless-core
```

## Getting Started

``` python
from http import HTTPStatus
from os import getenv

from artless import App, Request, Response, ResponseFactory


def get_template(username: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Say hello</title>
      </head>
      <body>
        <h1>Hello, {username}!</h1>
      </body>
    </html>
    """


def say_hello(request: Request, username: str) -> Response:
    available_formats = {
        "json": ResponseFactory.json({"hello": username}),
        "plain": ResponseFactory.plain(f"Hello, {username}!"),
        "html": ResponseFactory.html(get_template(username)),
    }

    format = request.query.get("format", ["plain"])[0]

    if format not in available_formats:
        return ResponseFactory.create(status=HTTPStatus.BAD_REQUEST)

    return available_formats[format]


def create_application() -> App:
    app = App()
    app.set_routes([("GET", r"^/hello/(?P<username>\w+)$", say_hello)])
    return app


application = create_application()

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    host = getenv("HOST", "127.0.0.1")
    port = int(getenv("PORT", 8000))

    with make_server(host, port, application) as httpd:
        print(f"Started WSGI server on {host}:{port}")
        httpd.serve_forever()
```

Run it:

``` shellsession
$ python3 app.py
Started WSGI server on 127.0.0.1:8000
```

Check it:

``` shellsession
$ curl http://127.0.0.1:8000/hello/Peter
Hello, Peter!

$ curl http://127.0.0.1:8000/hello/Peter?format=html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Say hello</title>
  </head>
  <body>
    <h1>Hello, Peter!</h1>
  </body>
</html>

$ curl http://127.0.0.1:8000/hello/Peter?format=json
{"hello": "Peter"}
```

Need more? See [documentation](https://pages.peterbro.su/py3-artless-core/) and [examples](https://git.peterbro.su/peter/py3-artless-core/src/branch/master/examples).

## Roadmap

- [ ] Add ASGI support.
- [ ] Add plugin support.
- [ ] Add cookies support.
- [ ] Add async interface.
- [ ] Add `multipart/form-data` support.
- [ ] Add test client.
- [ ] Add benchmarks.
- [ ] Add more examples.
- [x] Add Sphinx doc.

## Related projects

* [artless-template](https://pypi.org/project/artless-template/) - the artless and small template library for server-side rendering.
