
# Developer plugin generation status endpoint
from models import DevResponseNotReady, DevResponseReady, DeveloperMessage


from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
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

# allow frontend server to talk to this backend
# TODO: adjust according to frontend details
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
