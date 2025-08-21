from fastapi import FastAPI

app = FastAPI()

@app.post("/session")
def create_session():
    session = Session()  # creates new session
    return {
        "session_id": session.id_,
        "messages": session.get_messages()
    }