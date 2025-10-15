from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- 1. IMPORT THIS

# Your existing router imports
from single_application.github import router as github_router
from single_application.stackoverflow import router as stackoverflow_router
from single_application.hacker_news import router as hackernews_router
from single_application.devto import router as devto_router
from single_application.kaggle import router as kaggle_router
from single_application.codeforces import router as codeforces_router
from single_application.gitlab import router as gitlab_router

app = FastAPI(title="Passive AI Aggregator")

# vvvvvv 2. ADD THIS ENTIRE SECTION RIGHT HERE vvvvvv
origins = [
    "http://localhost:8001",  # The address of your HTML frontend
    "http://127.0.0.1:8001", # Also add the IP address version
    "http://0.0.0.0:8001",   # <-- ADD THIS LINE
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ^^^^^^ END OF THE NEW SECTION ^^^^^^


# Your existing routers
app.include_router(github_router, prefix="/github")
app.include_router(stackoverflow_router, prefix="/stackoverflow")
app.include_router(hackernews_router, prefix="/hackernews")
app.include_router(devto_router, prefix="/devto")
app.include_router(kaggle_router, prefix="/kaggle")
app.include_router(codeforces_router, prefix="/codeforces")
app.include_router(gitlab_router, prefix="/gitlab")

# Your existing endpoints
@app.get("/features")
async def features():
    return {
        "github": {
            "example_endpoint": "/github/repos",
            "description": "List your GitHub repositories"
        },
        "stackoverflow": {
            "example_endpoint": "/stackoverflow/featured",
            "description": "Get recent Stack Overflow feed for a user"
        },
        "hackernews": {
            "example_endpoint": "/hackernews/topstories",
            "description": "List top stories from Hacker News"
        },
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
        }
    }

@app.get("/")
async def root():
    return {"message": "Welcome to the Passive AI Aggregator! See /features for a summary."}
