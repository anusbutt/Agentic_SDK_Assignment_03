from pydantic import BaseModel

class UserContext(BaseModel):
    name: str
    uid: int
    is_premium_user: bool = False
    issue_type: str = "general"


class Message_output(BaseModel):
    response: str
    is_apology: bool

class Apology_output(BaseModel):
    reasoning: str
    is_apology: bool

