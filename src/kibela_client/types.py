from pydantic import BaseModel


class Budget(BaseModel):
    consumed: int
    cost: int
    remaining: int
