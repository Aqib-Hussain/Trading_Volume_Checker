from pydantic import BaseModel


class _ExecutedTradeBase(BaseModel):
    execution_id: str
