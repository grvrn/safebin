from pydantic import BaseModel

class PasteResponse(BaseModel):
    paste_key: str
    url: str