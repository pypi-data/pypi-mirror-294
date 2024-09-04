from fluid_sbom.internal.cache import (
    dual_cache,
)
import requests
from typing import (
    Any,
)


@dual_cache
def make_get(url: str, *, content: bool = False, **kwargs: Any) -> Any | None:
    response = requests.get(url, timeout=kwargs.pop("timeout", 20), **kwargs)
    if response.status_code != 200:
        return None
    if content:
        return response.content.decode("utf-8")

    return response.json()
