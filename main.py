from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Header
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
from routers import client
from dependencies import get_token_header
from routers.client import search_client, search_full_log
from db.models import client as cl

app = FastAPI()

app.include_router(client.router,
                   prefix="/client",
                   tags=["client"],
                   dependencies=[Depends(get_token_header)],
                   responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}})

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="Token")
crypt = CryptContext(schemes=["bcrypt"])
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                              detail="Credenciales invalidas",
                              headers={"WWW-Authenticate" : "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        id = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("id")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_client('id', id)

async def current_user(client: cl = Depends(auth_user)):
    clientLog = search_full_log('id', client.id)
    
    if clientLog.status != 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario Inactivo")
    
    return client

@app.post("/Token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    
    client = search_full_log('username', form.username)
    if not client:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    if not crypt.verify(form.password, client.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token = {"sub" : client.username,
                    "id" : client.id,
                    "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_DURATION)}
    
    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), 
        "token_type": "bearer",
        "username": client.username,
        ".issued": datetime.utcnow(),
        ".expires": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_DURATION)}

@app.get("/Token/me")
async def me(client: cl = Depends(current_user)):
    return client