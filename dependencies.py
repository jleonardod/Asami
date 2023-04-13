from fastapi import HTTPException, Header, status
from typing import Annotated
import main
import re
from db.models import client

async def get_token_header(Authorization: Annotated[str, Header()]):
  
    token = re.split(" ", Authorization)
    token = token[1]
    respuesta = await main.auth_user(token=token)
    
    if type(respuesta) != client.Client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token invalid")
