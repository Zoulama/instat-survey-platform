# /instat-survey-platform/schemas/base.py

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True

