from prometheus_client import Counter, Histogram
from functools import wraps
from time import time

REQUEST_COUNT = Counter('request_count', 'Total number of requests')
CALCULATION_COUNT = Counter('calculation_count', 'Total number of calculations')
REQUEST_TIME = Histogram('request_processing_seconds', 'Time spent processing request')
ERROR_COUNT = Counter('error_count', 'Total number of errors')
ENDPOINT_HITS = Counter('endpoint_hits', 'Hits per endpoint', ['endpoint'])

def timing_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time()
        result = await func(*args, **kwargs)
        REQUEST_TIME.observe(time() - start_time)
        return result
    return wrapper

def error_tracker(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            ERROR_COUNT.inc()
            raise
    return wrapper

def hit_counter(endpoint):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            ENDPOINT_HITS.labels(endpoint=endpoint).inc()
            return await func(*args, **kwargs)
        return wrapper
    return decorator