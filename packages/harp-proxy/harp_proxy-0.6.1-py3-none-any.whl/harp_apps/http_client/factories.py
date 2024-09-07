from httpx import AsyncClient
from whistle import IAsyncEventDispatcher

from harp.utils.services import factory
from harp_apps.http_client.settings import HttpClientSettings
from harp_apps.http_client.transport import AsyncFilterableTransport
from harp_apps.storage.types import IBlobStorage


def _resolve(x, *args, **kwargs):
    if hasattr(x, "build"):
        return x.build(*args, **kwargs)
    if len(args) or len(kwargs):
        raise ValueError(
            f"Cannot resolve {x} with args {args} and kwargs {kwargs}: parametrized lazy services must implement a build method."
        )
    return x


@factory(AsyncClient)
def AsyncClientFactory(
    self, settings: HttpClientSettings, dispatcher: IAsyncEventDispatcher, storage: IBlobStorage
) -> AsyncClient:
    httpx_transport = _resolve(settings.transport)
    httpx_transport = AsyncFilterableTransport(transport=httpx_transport, dispatcher=dispatcher)

    if settings.cache.enabled:
        from harp_apps.http_client.contrib.hishel.storages import AsyncStorage

        httpx_transport = _resolve(
            settings.cache.transport,
            transport=httpx_transport,
            controller=_resolve(settings.cache.controller),
            storage=AsyncStorage(
                storage,
                ttl=settings.cache.ttl,
                check_ttl_every=settings.cache.check_ttl_every,
            ),
        )

    return AsyncClient(transport=httpx_transport, timeout=settings.timeout)
