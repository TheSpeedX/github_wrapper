from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from datetime import datetime
from config.variables import GITHUB_OAUTH, JWT_CONFIG
from utils.token import generate_access_token
import uuid
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
    print(response.text)
    try:
        response = response.json()
        print(response)
        access_token = response.get('access_token')
        return {"access_token": generate_access_token(access_token)}
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Error Occured Retry OAuth") from e


@auth.get('/guest/token', tags=["auth"])
async def get_guest_token():
    username = str(uuid.uuid4())
    return {
        "access_token": generate_guest_access_token(username),
        "token_type": "Bearer",
        "access_token_expire":
        JWT_CONFIG["GUEST_TOKEN_EXPIRE_MINUTES"]*60,
    }
