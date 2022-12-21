from pydantic import BaseModel


class userModel(BaseModel):
    username: str
    name: str
    email: str
    pwd: str
    is_dev: bool


class requestModel(BaseModel):
    client: int
    req_type: str
    description: str
    creation_date: str
    was_attended: bool


class req_answerModel(BaseModel):
    request: int
    dev: int
    meet_link: str
    comment: str


class evaluationModel(BaseModel):
    request: int
    answer: int
    investment_return: float
    description: str


class c_resumeModel(BaseModel):
    description: str
    value: float
