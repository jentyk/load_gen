"""Loader tests."""
from http import HTTPStatus

import pytest

from load import main


@pytest.fixture(autouse=True)
def mocking(mocker):
    """Test mocks."""
    mocker.patch("load.cycle", iter)
    mocker.patch("config.config.FREQUENCY", 1000)


@pytest.mark.parametrize(
    "reqs",
    (
        {
            "url": "http://test.tst/blah",
            "http_method": "GET",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {},
        },
        {
            "url": "http://test.tst/blah",
            "http_method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {"key": "value"},
        },
        {
            "url": "http://test.tst/blah",
            "http_method": "PUT",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {"key": "value"},
        },
        {
            "url": "http://test.tst/blah",
            "http_method": "DELETE",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {"key": "value"},
        },
        {
            "url": "http://test.tst/blah",
            "http_method": "DELETE",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {"key": "value"},
        },
        {
            "url": "http://test.tst/blah",
            "http_method": "HEAD",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {"key": "value"},
        },
        {
            "url": "http://test.tst/blah",
            "http_method": "OPTIONS",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": {"key": "value"},
        },
    ),
)
def test_methods(mocker, httpx_mock, reqs):
    """Tests all http methods."""
    mocker.patch("config.config.REQUESTS", (reqs,))
    mocker.patch("config.config.CONCURRENT", (1,))
    httpx_mock.add_response(
        url=reqs["url"],
        method=reqs["http_method"],
        match_headers=reqs["headers"],
        json=reqs["data"],
        status_code=HTTPStatus.OK,
    )
    resp_stats = main()
    assert dict(resp_stats) == {HTTPStatus.OK: 1}


@pytest.mark.parametrize(
    "reqs,codes",
    (
        (
            (
                {
                    "url": "http://test.tst/foo",
                    "http_method": "GET",
                    "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                    "data": {},
                },
                {
                    "url": "http://test.tst/bar",
                    "http_method": "GET",
                    "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                    "data": {"baz": "qux"},
                },
                {
                    "url": "http://test.tst/foo",
                    "http_method": "GET",
                    "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                    "data": {"baz": "qux"},
                },
            ),
            (
                HTTPStatus.OK,
                HTTPStatus.NOT_FOUND,
                HTTPStatus.OK,
            ),
        ),
    ),
)
def test_concurrency(mocker, httpx_mock, reqs, codes):
    """Tests concurrency."""
    mocker.patch("config.config.REQUESTS", reqs)
    mocker.patch("config.config.CONCURRENT", (1, 2))
    for req, code in zip(reqs, codes):
        params = "?" if req["data"] else ""
        for k, v in req["data"].items():
            params = params + f"{k}={v}"
        httpx_mock.add_response(
            url=f"{req['url']}{params}",
            method=req["http_method"],
            match_headers=req["headers"],
            status_code=code,
        )
    resp_stats = main()
    assert dict(resp_stats) == {HTTPStatus.OK: 2, HTTPStatus.NOT_FOUND: 1}
