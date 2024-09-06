import base64
import io

import httpx
from PIL import Image

from midrasai.typedefs import base64_image, colbert, mode


class Midras:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://midras-api-worker.ajcardoza2000.workers.dev/",
    ):
        self.client = httpx.Client(base_url=base_url)
        self.api_key = api_key

    def embed_base64_images(
        self, base64_images: list[base64_image], mode: mode = "standard"
    ) -> list[colbert]:
        json = {"api_key": self.api_key, "mode": mode, "images": base64_images}
        response = self.client.post("/embed/images", json=json)
        print(response.text)
        json_response = response.json()
        print(json_response)
        return json_response["embeddings"]

    def embed_text(self, texts: list[str], mode: mode = "standard") -> list[colbert]:
        response = self.client.post(
            "/embed/text",
            json={"api_key": self.api_key, "mode": mode, "texts": texts},
        )
        return response.json()["embeddings"]

class AsyncMidras:
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://midras-api-worker.ajcardoza2000.workers.dev/",
    ):
        self.client = httpx.AsyncClient(base_url=base_url)
        self.api_key = api_key

    async def embed_base64_images(
        self, base64_images: list[base64_image], mode: mode = "standard"
    ) -> list[colbert]:
        json = {"api_key": self.api_key, "mode": mode, "images": base64_images}
        response = await self.client.post("/embed/images", json=json)
        print(response.text)
        json_response = response.json()
        print(json_response)
        return json_response["embeddings"]

    async def embed_text(self, texts: list[str], mode: mode = "standard") -> list[colbert]:
        response = await self.client.post(
            "/embed/text",
            json={"api_key": self.api_key, "mode": mode, "texts": texts},
        )
        return response.json()["embeddings"]
