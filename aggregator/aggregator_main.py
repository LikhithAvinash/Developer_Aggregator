from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- Import routers from 'single_application' ---
from single_application.github import router as old_github_router
from single_application.stackoverflow import router as old_stackoverflow_router
from single_application.hacker_news import router as old_hackernews_router
from single_application.devto import router as devto_router
from single_application.kaggle import router as kaggle_router
from single_application.codeforces import router as codeforces_router
from single_application.gitlab import router as gitlab_router

# --- Import routers from 'endpoints' (from your ep.py file) ---
from endpoints.pypi import router as pypi_router
from endpoints.npm import router as npm_router
from endpoints.github_ep import router as new_github_router
from endpoints.hn import router as new_hn_router
from endpoints.reddit import router as reddit_router
from endpoints.so import router as new_stackoverflow_router

app = FastAPI(
    title="Developer AI Agent Aggregator",
    description="A single API to fetch data from multiple developer platforms.",
    version="1.0.0"
)

# --- Add CORS Middleware ---
# This is crucial for your frontend to be able to talk to the backend
origins = [
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://0.0.0.0:8001",
    "ttps://developer-aggregator-kuqj.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include all routers with a specific prefix ---

# Services from your first set
app.include_router(devto_router, prefix="/devto", tags=["DEV.to"])
app.include_router(kaggle_router, prefix="/kaggle", tags=["Kaggle"])
app.include_router(codeforces_router, prefix="/codeforces", tags=["Codeforces"])
app.include_router(gitlab_router, prefix="/gitlab", tags=["GitLab"])

# Services from your new ep.py file
app.include_router(pypi_router, prefix="/pypi", tags=["PyPI"])
app.include_router(npm_router, prefix="/npm", tags=["npm"])
app.include_router(reddit_router, prefix="/reddit", tags=["Reddit"])

# We use the new routers for github, hn, and stackoverflow as they might be more up-to-date
app.include_router(old_github_router, prefix="/github", tags=["GitHub"])
app.include_router(old_hackernews_router, prefix="/hackernews", tags=["Hacker News"])
app.include_router(old_stackoverflow_router, prefix="/stackoverflow", tags=["Stack Overflow"])

@app.get("/features", tags=["Features"])
async def features():
    """Provides a summary of all available endpoints."""
    return {
        "devto": {
            "example_endpoint": "/devto/articles",
            "description": "Fetch latest DEV.to articles"
        },
        "kaggle": {
            "example_endpoint": "/kaggle/datasets",
            "description": "List trending Kaggle datasets"
        },
        "codeforces": {
            "example_endpoint": "/codeforces/contests",
            "description": "Get upcoming Codeforces contests"
        },
        "gitlab": {
            "example_endpoint": "/gitlab/projects",
            "description": "List your GitLab projects"
        },
        "pypi": {
            "example_endpoint": "/pypi/latest",
            "description": "Get the latest packages from PyPI"
        },
        "npm": {
            "example_endpoint": "/npm/search?text=react",
            "description": "Search for packages on npm"
        },
        "reddit": {
            "example_endpoint": "/reddit/top/programming",
            "description": "Get top posts from a specified subreddit"
        },
        "github": {
            "example_endpoint": "/github/repos",
            "description": "List your GitHub repositories"
        },
        "hackernews": {
            "example_endpoint": "/hackernews/topstories",
            "description": "List top stories from Hacker News"
        },
        "stackoverflow": {
            "example_endpoint": "/stackoverflow/questions",
            "description": "Get recent Stack Overflow questions"
        }
    }

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Aggregator API! All services are running."}
