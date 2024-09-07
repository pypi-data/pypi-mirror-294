from abc import ABC, abstractmethod

import httpx
from pdf2image import convert_from_path
from PIL.Image import Image

from midrasai._constants import CLOUD_URL
from midrasai.client._vector_module import AsyncQdrantModule, QdrantModule
from midrasai.client.utils import base64_encode_image_list
from midrasai.typedefs import Base64Image, MidrasResponse, Mode


class BaseMidras(ABC):
    def validate_response(self, response: httpx.Response) -> MidrasResponse:
        if response.status_code >= 500:
            raise ValueError(response.text)
        return MidrasResponse(**response.json())

    def embed_pdf(
        self, pdf_path: str, batch_size: int = 10, include_images: bool = False
    ) -> MidrasResponse:
        images = convert_from_path(pdf_path)
        embeddings = []
        total_spent = 0

        for i in range(0, len(images), batch_size):
            image_batch = images[i : i + batch_size]
            response = self.embed_pil_images(image_batch)
            embeddings.extend(response.embeddings)
            total_spent += response.credits_spent

        return MidrasResponse(
            credits_spent=total_spent,
            embeddings=embeddings,
            images=images if include_images else None,
        )

    def embed_pil_images(
        self, pil_images: list[Image], mode: Mode = "standard"
    ) -> MidrasResponse:
        base64_images = base64_encode_image_list(pil_images)
        return self.embed_base64_images(base64_images, mode)

    @abstractmethod
    def embed_base64_images(): ...


class Midras(BaseMidras):
    def __init__(self, api_key: str, qdrant: str, *args, **kwargs):
        self.api_key = api_key
        self.client = httpx.Client(base_url=CLOUD_URL)
        self.index = QdrantModule(location=qdrant, *args, **kwargs)

    def embed_base64_images(
        self, base64_images: list[Base64Image], mode: Mode = "standard"
    ) -> MidrasResponse:
        json = {
            "api_key": self.api_key,
            "mode": mode,
            "inputs": base64_images,
            "image_input": True,
        }
        response = self.client.post("", json=json, timeout=180)
        return self.validate_response(response)

    def embed_text(self, texts: list[str], mode: Mode = "standard") -> MidrasResponse:
        json = {
            "api_key": self.api_key,
            "mode": mode,
            "inputs": texts,
            "image_input": False,
        }
        response = self.client.post("", json=json, timeout=180)
        return self.validate_response(response)

    def query_text(self, collection_name: str, text: str):
        query_vector = self.embed_text([text]).embeddings[0]
        return self.index.query(collection_name, query_vector)


class AsyncMidras(BaseMidras):
    def __init__(self, api_key: str, qdrant: str, *args, **kwargs):
        self.api_key = api_key
        self.client = httpx.AsyncClient(base_url=CLOUD_URL)
        self.index = AsyncQdrantModule(location=qdrant * args, **kwargs)

    async def embed_base64_images(
        self, base64_images: list[Base64Image], mode: Mode = "standard"
    ) -> MidrasResponse:
        json = {
            "api_key": self.api_key,
            "mode": mode,
            "inputs": base64_images,
            "image_input": True,
        }
        response = await self.client.post("", json=json, timeout=180)
        return self.validate_response(response)

    async def embed_text(
        self, texts: list[str], mode: Mode = "standard"
    ) -> MidrasResponse:
        json = {
            "api_key": self.api_key,
            "mode": mode,
            "inputs": texts,
            "image_input": False,
        }
        response = await self.client.post("", json=json, timeout=180)
        return self.validate_response(response)

    async def query_text(self, collection_name: str, text: str):
        query_vector = (await self.embed_text([text])).embeddings[0]
        return await self.index.query(collection_name, query_vector)
