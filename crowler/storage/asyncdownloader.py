import asyncio
from collections import deque
from google.cloud.storage import Blob
from collections.abc import Iterable


def download(blobs: Iterable[Blob], chunkedSizeLimit=100):
    chunk = deque()
    chunkedSize = 0

    for blob in blobs:
        chunk.append(blob)
        chunkedSize += 1
        if chunkedSize >= chunkedSizeLimit:
            results = asyncio.run(_download_multi(chunk))
            chunk = deque()
            chunkedSize = 0
            for result in results:
                yield result
    if chunkedSize > 0:
        results = asyncio.run(_download_multi(chunk))
        chunk = deque()
        chunkedSize = 0
        for result in results:
            yield result


async def _download_multi(blobs: Iterable[Blob]):
    results = await asyncio.gather(*[_download_async(blob) for blob in blobs])
    return results


async def _download_async(blob: Blob):
    await asyncio.sleep(0)
    return blob.download_as_string()
