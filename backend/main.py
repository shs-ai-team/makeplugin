
# Developer plugin generation status endpoint
from models import DevResponseNotReady, DevResponseReady, DeveloperMessage
import os
from dotenv import load_dotenv

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from uuid import UUID
import json

from session import Session
from models import (
    CreateSessionResponse,
    GetSessionResponse,
    UserInputRequest,
    ConsultantResponse,
    DevResponseNotReady,
    DevResponseReady,
    UserMessage,
    ConsultantMessage,
)
from wordpress_consultant_agent import WordPressConsultantAgent
from wordpress_developer_agent import WordpressDeveloperAgent   

app = FastAPI()

# Get the frontend URL from an environment variable
# Provide a default for local development
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

# This is the list of approved origins
origins = [
    frontend_url,
]

# allow frontend server to talk to this backend
# need to adjust according to frontend details
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/session", response_model=CreateSessionResponse)
def create_session():
    '''
    Creates a new plugin generation chat session and returns it
    '''
    session = Session()
    return CreateSessionResponse(
        session_id=session.id_,
        messages=session.get_messages()
    )


@app.get("/sessions")
def get_all_sessions():
    return Session.get_all_session_ids()


@app.get("/session/{session_id}", response_model=GetSessionResponse)
def get_session(session_id: UUID):
    '''
    Gets a session given its ID
    '''
    session = Session(session_id=str(session_id))

    return GetSessionResponse(
        session_id=session.id_,
        messages=session.get_messages()
    )

@app.post("/session/{session_id}/consultant_response", response_model=ConsultantResponse)
def consultant_response(session_id: UUID, user_input: UserInputRequest, background_tasks: BackgroundTasks):
    
    session = Session(session_id=str(session_id))

    ai_response: ConsultantMessage = WordPressConsultantAgent.consult(user_message=user_input.message, session=session)

    requirements_finalized: bool = ai_response.requirements_finalized == True
    
    print(f"LOG: Requirements finalized: {requirements_finalized}.")
    if requirements_finalized:
        requirements = ai_response.requirements

        # start development through developer agent asyncronously
        print(f"LOG: Begining AI dev task")
        background_tasks.add_task(WordpressDeveloperAgent.generate_plugin_files, requirements, session)
    
    return ConsultantResponse(
        message=ai_response,
    )


@app.post("/session/{session_id}/dev_response", response_model=None)
def dev_response(session_id: UUID):
    """
    Checks if the developer has finished generating the plugin zip for this session.
    Returns {"success": false} if not ready, or {"success": true, message: {...}} if ready.
    """
    session = Session(session_id=str(session_id))
    messages = session.get_messages()

    if not messages:
        return DevResponseNotReady()

    latest_message = messages[-1]
    if latest_message["role"] != "developer":
        return DevResponseNotReady()
    
    return DevResponseReady(message=DeveloperMessage(
            content=latest_message["content"],
            zip_id=latest_message["zip_id"],
            raw_response=latest_message["raw_response"]
        ))


@app.get("/session/{session_id}/download_zip/{zip_id}")
def download_zip(session_id: UUID, zip_id: int):

    zip_path = Session.get_zip_path(str(session_id), zip_id)
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="File not found")    
    
    return FileResponse(
        path=zip_path,
        filename=os.path.basename(zip_path),
        media_type="application/zip",
    )


# --------- FOR FRONTEND HOSTING --------------
from pathlib import Path
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Base dir: /app (container), adjust according to your structure
BASE_DIR = Path(__file__).resolve().parent.parent  # -> repo root (/app)
FRONTEND_BUILD = BASE_DIR / "frontend" / "build"
INDEX_FILE = FRONTEND_BUILD / "index.html"

if FRONTEND_BUILD.exists() and INDEX_FILE.exists():
    # Serve static assets (React build puts hashed assets in build/static)
    static_dir = FRONTEND_BUILD / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/{full_path:path}")
    async def spa_router(request: Request, full_path: str):
        """
        If requested file exists in build, serve it.
        Otherwise return index.html so React Router takes over.
        """
        # Root path
        if full_path == "" or full_path is None:
            return FileResponse(str(INDEX_FILE))

        candidate = FRONTEND_BUILD / full_path

        # If it's a directory, serve index.html (SPA)
        if candidate.is_dir():
            return FileResponse(str(INDEX_FILE))

        # If file exists (e.g. /favicon.ico or /static/js/xxx.js), serve it
        if candidate.exists():
            return FileResponse(str(candidate))

        # Otherwise serve index.html for SPA route
        return FileResponse(str(INDEX_FILE))
# ---------------------------------------------------------
