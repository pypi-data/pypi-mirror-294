import httpx
from httpx import AsyncClient

from gravybox.betterstack import collect_logger

logger = collect_logger()

TIMEOUT = 120


class AsyncRequestManager:
    """
    Singleton wrapper for an async http request client
    expects to be initialized once during FastAPI startup
    expects to be closed once during FastAPI shutdown
    use the static methods, avoid touching internal_* variables and functions
    """

    def __init__(self):
        limits = httpx.Limits(max_keepalive_connections=None, max_connections=None, keepalive_expiry=None)
        timeout = httpx.Timeout(TIMEOUT)
        self.internal_request_client: AsyncClient = AsyncClient(timeout=timeout, limits=limits)

    def __enter__(self):
        AsyncRequestManager.initialize()
        return AsyncRequestManager.client()

    def __exit__(self, type, value, traceback):
        AsyncRequestManager.shutdown()

    @staticmethod
    def client() -> AsyncClient:
        global INTERNAL_ASYNC_REQUEST_SINGLETON
        if INTERNAL_ASYNC_REQUEST_SINGLETON is None:
            raise RuntimeError("AsyncClient.initialize() must be called before AsyncClient.client()")
        return INTERNAL_ASYNC_REQUEST_SINGLETON.internal_request_client

    @staticmethod
    def initialize():
        logger.info("initializing request client")
        global INTERNAL_ASYNC_REQUEST_SINGLETON
        INTERNAL_ASYNC_REQUEST_SINGLETON = AsyncRequestManager()

    @staticmethod
    async def shutdown():
        logger.info("shutting down request client")
        global INTERNAL_ASYNC_REQUEST_SINGLETON
        await INTERNAL_ASYNC_REQUEST_SINGLETON.internal_request_client.aclose()


INTERNAL_ASYNC_REQUEST_SINGLETON: AsyncRequestManager | None = None
