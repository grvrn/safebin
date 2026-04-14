from fastapi import APIRouter

from backend.objects.requests import PasteRequest
from backend.service import encrypt_and_send, decrypt_and_read

router = APIRouter()

@router.post("/v1/post/")
async def post_paste(request: PasteRequest):
    result = encrypt_and_send(request.content, name=request.title)
    return {"result": result}

@router.get("/v1/read/{paste_key}")
async def read_paste(paste_key: str):
    content = decrypt_and_read(paste_key)
    return {"content": content}