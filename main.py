from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Header
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.staticfiles import StaticFiles
from routers import client
from dependencies import get_token_header

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

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "jreboot" : {
        "username": "jreboot",
        "full_name": "Leonardo Diaz",
        "email": "jldiaz9623@gmail.com",
        "disabled" : False,
        "password" : "$2a$12$Ovs/Mppt0wc/0scUUP2kq.up36q6vFO/ls1kV/H3phxQz04SAV6De"
    },
    "jreboot2" : {
        "username": "jreboot2",
        "full_name": "Leonardo Diaz 2",
        "email": "jldiaz96232@gmail.com",
        "disabled" : True,
        "password" : "$2a$12$8HoNvt2Xu1MbRpiTNPz7oe5mPkfZmLGctz7KFCwllo9Hv7V12GVjS"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                              detail="Credenciales invalidas",
                              headers={"WWW-Authenticate" : "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario Inactivo")
    
    return user

@app.post("/Token")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token = {"sub" : user.username,
                    "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_DURATION)}
    
    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), 
        "token_type": "bearer",
        "username": user.username,
        ".issued": datetime.utcnow(),
        ".expires": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_DURATION)}

@app.get("/Token/me")
async def me(user: User = Depends(current_user)):
    return user