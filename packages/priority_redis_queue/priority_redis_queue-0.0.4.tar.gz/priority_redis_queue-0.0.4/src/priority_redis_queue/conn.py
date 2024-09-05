from typing import Any

import redis


def get_redis_connection(host: str, port: int) -> Any:
    """
    Return the redis connection
    """
    main_redis_connections_pool = redis.ConnectionPool(host=host, port=port, db=0)
    redis_connection = redis.Redis(
        connection_pool=main_redis_connections_pool,
        socket_timeout=2,
        socket_connect_timeout=2,
    )
    return redis_connection
