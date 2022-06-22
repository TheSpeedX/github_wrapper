from fastapi import APIRouter, Depends
from utils.token import get_current_token, get_current_username
from models.repo import CreateRepoModel, UpdateTopicsModel
from typing import Dict, Optional
import httpx

repo = APIRouter()

BASE_URL = "https://api.github.com"


def remove_filter(obj):
    """Removes keys from nested dictionaries
    where the string api.github.com is found"""
    if isinstance(obj, (tuple, list, set)):
        t = type(obj)
        obj = t(remove_filter(a) for a in obj)
    elif isinstance(obj, dict):
        obj = {k: remove_filter(v) for k, v in obj.items()
               if isinstance(v, str) and "api.github.com" not in v}
    return obj


async def call_github_api(
    token: str,
    request_type: str,
    url_path: str,
    json: Dict = None
) -> Dict:
    """Hits the github API with given path and parameters"""
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
        return remove_filter(response.json())


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


@repo.get('/topics', tags=["Topics"])
async def list_topics(
        repo_name: str,
        username: Optional[str] = None,
        current_username: str = Depends(get_current_username),
        access_token: str = Depends(get_current_token)
):
    if not username:
        username = current_username
    return await call_github_api(
        token=access_token,
        request_type="GET",
        url_path=f'repos/{username}/{repo_name}/topics'
    )


@repo.put('/topics', tags=["Topics"])
async def update_topics(
        topic_info: UpdateTopicsModel,
        current_username: str = Depends(get_current_username),
        access_token: str = Depends(get_current_token)
):
    username = topic_info.username
    repo_name = topic_info.repo_name
    topics = topic_info.topics
    if not username:
        username = current_username
    return await call_github_api(
        token=access_token,
        request_type="PUT",
        url_path=f'repos/{username}/{repo_name}/topics',
        json={"names": topics}
    )


@repo.get('/contributors', tags=["Insights"])
async def list_contributors(
        repo_name: str,
        username: Optional[str] = None,
        current_username: str = Depends(get_current_username),
        access_token: str = Depends(get_current_token)
):
    if not username:
        username = current_username
    return await call_github_api(
        token=access_token,
        request_type="GET",
        url_path=f'repos/{username}/{repo_name}/contributors'
    )


@repo.get('/stargazers', tags=["Insights"])
async def list_stargazers(
        repo_name: str,
        username: Optional[str] = None,
        current_username: str = Depends(get_current_username),
        access_token: str = Depends(get_current_token)
):
    if not username:
        username = current_username
    return await call_github_api(
        token=access_token,
        request_type="GET",
        url_path=f'repos/{username}/{repo_name}/stargazers'
    )


@repo.get('/repo_with_stars_and_forks', tags=["Insights"])
async def repo_with_stars_and_forks(
        username: Optional[str] = None,
        current_username: str = Depends(get_current_username),
        access_token: str = Depends(get_current_token)
):
    if not username:
        username = current_username
    response = await call_github_api(
        token=access_token,
        request_type="GET",
        url_path=f'search/repositories?q=user:{username} stars:>5 forks:>5'
    )
    return response['items']
