import json
from functools import wraps
from json import JSONDecodeError
from typing import Any, Callable

from pydantic import BaseModel
from redis import Redis, RedisError

redis_client: Redis = Redis(host="localhost", port=6379, db=0, decode_responses=True)


def cache_response(expire_time_seconds: int = 345600, key_prefix: str = "") -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                cache_key: str = (
                    f"{key_prefix}:{func.__name__}:{str(args)}:{str(kwargs)}"
                )

                try:
                    cached_response = redis_client.get(cache_key)
                    if cached_response:
                        return json.loads(cached_response)
                except JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    redis_client.delete(cache_key)
                except RedisError as e:
                    print(f"Redis error: {e}")
                    return await func(*args, **kwargs)

                response = await func(*args, **kwargs)

                try:
                    if isinstance(response, BaseModel):
                        json_response = response.model_dump_json()
                    elif isinstance(response, list) and all(
                        isinstance(x, BaseModel) for x in response
                    ):
                        json_response = json.dumps(
                            [item.model_dump() for item in response]
                        )
                    else:
                        json_response = json.dumps(response)

                    if expire_time_seconds is not None:
                        redis_client.setex(
                            cache_key, expire_time_seconds, json_response
                        )
                    else:
                        redis_client.set(cache_key, json_response)
                except Exception as e:
                    print(f"Error setting cache: {e}")

                return response

            except Exception as e:
                print(f"Unexpected error: {e}")
                return await func(*args, **kwargs)

        return wrapper

    return decorator
