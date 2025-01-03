import json
from unittest.mock import patch

import pytest
from redis import RedisError

from cache.cache import cache_response


class MockBaseModel:
    def model_dump_json(self):
        return json.dumps({"id": 1, "name": "test"})

    def model_dump(self):
        return {"id": 1, "name": "test"}


async def mock_function(param1, param2):
    return {"data": f"{param1}_{param2}"}


async def mock_model_function():
    return MockBaseModel()


async def mock_model_list_function():
    return [MockBaseModel(), MockBaseModel()]


@pytest.fixture
def mock_redis():
    with patch("cache.cache.redis_client") as mock:
        yield mock


@pytest.mark.asyncio
async def test_basic_cache_hit(mock_redis):
    mock_redis.get.return_value = '{"data": "cached_value"}'

    cached_func = cache_response()(mock_function)
    result = await cached_func("test1", "test2")

    assert result == {"data": "cached_value"}
    mock_redis.get.assert_called_once()
    assert not mock_redis.set.called
    assert not mock_redis.setex.called


@pytest.mark.asyncio
async def test_cache_miss(mock_redis):
    mock_redis.get.return_value = None

    cached_func = cache_response(expire_time_seconds=60)(mock_function)
    result = await cached_func("test1", "test2")

    assert result == {"data": "test1_test2"}
    mock_redis.setex.assert_called_once()
    called_key = mock_redis.setex.call_args[0][0]
    assert "mock_function" in called_key


@pytest.mark.asyncio
async def test_redis_error_fallback(mock_redis):
    mock_redis.get.side_effect = RedisError("Connection failed")

    cached_func = cache_response()(mock_function)
    result = await cached_func("test1", "test2")

    assert result == {"data": "test1_test2"}
    mock_redis.get.assert_called_once()


@pytest.mark.asyncio
async def test_corrupted_cache_handling(mock_redis):
    mock_redis.get.return_value = "invalid{json"

    cached_func = cache_response()(mock_function)
    result = await cached_func("test1", "test2")

    assert result == {"data": "test1_test2"}
    mock_redis.delete.assert_called_once()


@pytest.mark.asyncio
async def test_permanent_cache(mock_redis):
    mock_redis.get.return_value = None

    cached_func = cache_response(expire_time_seconds=None)(mock_function)
    await cached_func("test1", "test2")

    mock_redis.set.assert_called_once()
    mock_redis.setex.assert_not_called()
