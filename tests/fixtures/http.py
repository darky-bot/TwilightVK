import pytest
import pytest_asyncio

from twilight_vk.http.async_http import Http

@pytest.fixture
def http_params():
    return {
        "test_key": "123",
        "test_str": "abc123"
    }

@pytest.fixture
def http_data():
    return {
        "test_key": "test_value",
        "test_str": "abcd"
    }

@pytest_asyncio.fixture
async def http_client():
    httpClient = Http(headers={"X-Test": "test"}, timeout=10)
    yield httpClient
    await httpClient.close()