from fastapi import APIRouter, Depends
from utils.token import get_current_token, get_current_username
from models.repo import CreateRepoModel, UpdateTopicsModel
from typing import Dict, Optional
import httpx

repo = APIRouter()

BASE_URL = "https://api.github.com"


async def call_github_api(
    token: str,
    request_type: str,
    url_path: str,
    json: Dict = None
) -> Dict:
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    with httpx.Client(headers=headers) as client:
        if json:
            request = client.build_request(
                request_type, f"{BASE_URL}/{url_path}", json=json)
        else:
            request = client.build_request(
                request_type, f"{BASE_URL}/{url_path}")
        response = client.send(request)
        return response.json()
    # TODO: Remove fields that have api.github.com


@repo.post('/repo', tags=["Repo"])
async def create_repo(
        repo_data: CreateRepoModel,
        access_token: str = Depends(get_current_token)
):
    return await call_github_api(
        token=access_token,
        request_type="POST",
        url_path='user/repos',
        json=dict(repo_data),
    )


@repo.get('/repo', tags=["Repo"])
async def list_repos(
        username: Optional[str] = None,
        current_username: str = Depends(get_current_username),
        access_token: str = Depends(get_current_token)
):
    if not username:
        username = current_username
    return await call_github_api(
        token=access_token,
        request_type="GET",
        url_path=f'users/{username}/repos'
    )

