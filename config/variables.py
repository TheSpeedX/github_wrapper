from dotenv import load_dotenv
import os

load_dotenv()

JWT_CONFIG = {
    "SECRET_KEY": os.environ.get("SECRET_KEY"),
    "ALGORITHM": "HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES": 24*60
}

GITHUB_OAUTH = {
    "CLIENT_ID": "7d0f1789313000dbd54d",
    "CLIENT_SECRET": os.environ.get("CLIENT_SECRET"),
    "AUTHORIZE_URI": 'https://github.com/login/oauth/authorize',
    "TOKEN_URI": 'https://github.com/login/oauth/access_token',
    "REDIRECT_URI": 'http://127.0.0.1/github/callback'
}
