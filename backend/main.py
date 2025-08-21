from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import UUID

from session import Session
from models import (
    CreateSessionResponse,
    GetSessionResponse,
    UserInputRequest,
    ConsultantResponse,
    DevResponseNotReady,
    DevResponseReady,
    UserMessage,
)

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
def consultant_response(session_id: UUID, user_input: UserInputRequest):
    
    # get the session
    session = Session(session_id=str(session_id))

    # Add user message to session
    user_message = UserMessage(user_input.message)
    session.add_message(role=user_message.role, content=user_message.content)

    # Consult
    ai_response = 

