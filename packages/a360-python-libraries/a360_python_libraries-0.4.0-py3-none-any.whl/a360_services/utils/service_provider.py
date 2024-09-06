import httpx
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from ..settings import settings
from .services_list import Services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class ServiceProvider:
    def __init__(self, client: httpx.Client, token: str = None):
        self.client = client
        self.token = token

    def fetch_data(self, service: Services, request_path: str) -> dict:
        headers = {}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = self.client.get(
            f"{settings.PROJECT_HOST_SCHEME}://{service.value}/services/{service.name}{request_path}",
            headers=headers)
        response.raise_for_status()
        return response.json()


def get_service_provider(token: str = Depends(
        oauth2_scheme)) -> ServiceProvider:
    client = httpx.Client()
    return ServiceProvider(client=client, token=token)
