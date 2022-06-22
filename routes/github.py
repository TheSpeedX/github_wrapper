from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from config.variables import GITHUB_OAUTH
from utils.token import generate_access_token
from oauthlib.oauth2 import WebApplicationClient
import httpx

auth = APIRouter()


@auth.get('/login', tags=["github"])
async def start_github_login(request: Request):
    client = WebApplicationClient(GITHUB_OAUTH['CLIENT_ID'])
    uri = client.prepare_request_uri(
        GITHUB_OAUTH['AUTHORIZE_URI'],
        redirect_uri=request.url_for('callback'),
        scope=['read:user', 'repo']
    )
    return RedirectResponse(uri)


@auth.get('/callback', tags=["github"])
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_OAUTH['TOKEN_URI'],
            json={
                "client_id": GITHUB_OAUTH['CLIENT_ID'],
                "client_secret": GITHUB_OAUTH['CLIENT_SECRET'],
                "code": code,
                "redirect_uri": GITHUB_OAUTH["REDIRECT_URI"],
            },
            headers={"Accept": "application/json"}
        )
        try:
            response = response.json()
            print(response)
            access_token = response.get('access_token')
            user_info = await client.get(
                "https://api.github.com/user",
                headers={
                    "Accept": "application/vnd.github.v3+json",
                    "Authorization": f"token {access_token}"
                }
            )
            user_info = user_info.json()
            print(user_info)
            username = user_info['login']
            return {
                "access_token": generate_access_token(access_token, username)
            }
        except Exception as e:
            raise HTTPException(
                status_code=401, detail="Error Occured Retry OAuth") from e
