from pydantic import BaseModel


class _OrderBase(BaseModel):
    timestamp: int
    message_type : str
    order_id : str
