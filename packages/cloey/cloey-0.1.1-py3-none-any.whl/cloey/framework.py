from fastapi import FastAPI, Form
from pydantic import BaseModel
from typing import Optional

SESSIONS = {}


class Cloey:
    def __init__(self):
        self.routes = {}

    def route(self, step):
        def decorator(func):
            self.routes[step] = func
            return func

        return decorator

    def start(self, session_id, initial_step):
        SESSIONS[session_id] = {'step': initial_step, 'data': {}}
        return self.routes[initial_step](session_id)

    def handle_request(self, session_id, user_input):
        session = SESSIONS.get(session_id)
        if not session:
            return self.start(session_id, 'start')
        step = session['step']
        return self.routes[step](session_id, user_input)

    def next_step(self, session_id, next_step):
        SESSIONS[session_id]['step'] = next_step


app = FastAPI()
cloey = Cloey()


# Define USSD request body model
class USSDRequest(BaseModel):
    sessionId: str
    phoneNumber: str
    networkCode: str
    serviceCode: str
    text: Optional[str] = ""


@app.post("/")
def ussd_handler(ussd_request: USSDRequest):
    session_id = ussd_request.sessionId
    user_input = ussd_request.text.strip()  # Get the user input (strip trailing spaces)

    # Handle the USSD request
    response = cloey.handle_request(session_id, user_input)
    return {"message": response}
