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
    return Session.get_all_sessions()


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

    ai_response: dict = WordPressConsultantAgent.consult(user_message=user_input.message, session=session)

    requirements_finalized: bool = ai_response["requirements_finalized"] == True
    
    if requirements_finalized:
        requirements = ai_response["requirements"]

        # start development through developer agent asyncronously
        background_tasks.add_task(WordpressDeveloperAgent.generate_plugin_files, requirements)
    
    return ConsultantResponse(
        message=ConsultantMessage(
            content=str(json.dumps(ai_response, indent=2)),
            requirements_finalized=requirements_finalized,
        )
    )

    



