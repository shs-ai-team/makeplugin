from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from uuid import UUID


class ConsultantMessage(BaseModel):
    role: Literal["consultant"] = "consultant"
    content: str
    requirements_finalized: bool = False


class UserMessage(BaseModel):
    role: Literal["user"] = "user"
    content: str


class DeveloperMessage(BaseModel):
    role: Literal["developer"] = "developer"
    content: str
    zip_id: int

ChatMessage = ConsultantMessage | UserMessage | DeveloperMessage  # polymorphic message type


## --- API Models ---

class CreateSessionResponse(BaseModel):
    session_id: UUID
    messages: List[ConsultantMessage]


class GetSessionResponse(BaseModel):
    session_id: UUID
    messages: List[ChatMessage]


class UserInputRequest(BaseModel):
    message: str


class ConsultantResponse(BaseModel):
    message: ConsultantMessage


class DevResponseNotReady(BaseModel):
    success: Literal[False]
    
class DevResponseReady(BaseModel):
    success: Literal[True]
    message: DeveloperMessage


