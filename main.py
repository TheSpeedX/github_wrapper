from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from routes.github import auth
from routes.repo import repo

app = FastAPI(title="COMETLabs Github Wrapper")

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=RedirectResponse)
async def home():
    return "/docs"


app.include_router(auth, prefix="/github")
app.include_router(repo, prefix="/repos")
