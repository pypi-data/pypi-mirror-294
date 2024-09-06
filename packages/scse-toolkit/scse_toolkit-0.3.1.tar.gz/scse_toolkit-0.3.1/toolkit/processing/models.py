from pydantic import BaseModel, ConfigDict


class Root(BaseModel):
    model_config = ConfigDict(extra="allow")

    version: str
    utcnow: str


class Task(BaseModel):
    id: str
    state: str
    result: object | None = None
