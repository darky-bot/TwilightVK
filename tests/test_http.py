import pytest
import pytest_asyncio
import pytest_httpbin

from aiohttp import ClientResponse
from http import HTTPStatus

from tests.fixtures.http import (
    http_client,
    http_params,
    http_data,
    Http
)

@pytest.mark.asyncio
async def test_init_session(http_client: Http,
                            httpbin):
    assert http_client.headers == {"X-Test": "test"}
    assert http_client.timeout == 10
    assert http_client.session is None

@pytest.mark.asyncio
async def test_http_get_raw(http_client: Http,
                            http_params: dict,
                            httpbin):
    response = await http_client.get(
        url = f"{httpbin.url}/get",
        params = http_params,
        raw = True
    )
    assert isinstance(response, ClientResponse)
    assert response.status == HTTPStatus.OK
    _json_response: dict = await response.json()
    assert _json_response.get("args") == http_params
    

@pytest.mark.asyncio
async def test_http_get_json(http_client: Http,
                             http_params: dict,
                             httpbin):
    response = await http_client.get(
        url = f"{httpbin.url}/get",
        params = http_params,
        raw = False
    )
    assert isinstance(response, dict)
    assert response.get("args") == http_params
    assert response.get("headers").get("X-Test") == "test"

@pytest.mark.asyncio
async def test_http_post_raw(http_client: Http,
                             http_params: dict,
                             http_data: dict,
                             httpbin):
    response = await http_client.post(
        url = f"{httpbin.url}/post",
        data = http_data,
        params = http_params,
        raw = True
    )
    assert isinstance(response, ClientResponse)
    assert response.status == HTTPStatus.OK
    _json_response: dict = await response.json()
    assert _json_response.get("json") == http_data
    assert _json_response.get("args") == http_params

@pytest.mark.asyncio
async def test_http_post_json(http_client: Http,
                             http_params: dict,
                             http_data: dict,
                             httpbin):
    response = await http_client.post(
        url = f"{httpbin.url}/post",
        data = http_data,
        params = http_params,
        raw = False
    )
    assert isinstance(response, dict)
    assert response["json"] == http_data
    assert response["args"] == http_params
    assert response["headers"]["X-Test"] == "test"

@pytest.mark.asyncio
async def test_close_session(http_client: Http):
    await http_client._get_session()
    assert http_client is not None
    assert not http_client.session.closed
    await http_client.close()
    assert http_client.session is None