from pydantic import BaseModel

class PasteRequest(BaseModel):
    content: str
    title: str | None = None
    