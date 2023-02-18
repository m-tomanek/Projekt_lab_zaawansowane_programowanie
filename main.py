import math
import secrets
from datetime import datetime

from PIL import Image, ImageChops
from fastapi import Depends, FastAPI, HTTPException, status, security
from fastapi.security import HTTPBasicCredentials, HTTPBasic

app = FastAPI()
security = HTTPBasic()

def is_prime(lp_Liczba):
    for i in range(2, int(math.sqrt(lp_Liczba)) + 1):
        if (lp_Liczba % i) == 0:
            return "Liczba nie jest liczba pierwsza"
    return "Liczba jest liczba pierwsza"


@app.get("/lp/{lp_Liczba}")
async def czytaj_lp(lp_Liczba: int):
    if lp_Liczba > 9223372036854775807:
        return {"Liczba poza zakresem"}
    if lp_Liczba < 0:
        return {"Wprowadzona liczba nie jest liczba naturalna"}
    else:
        result = is_prime((lp_Liczba))
        return {"LP_Liczba": result}


@app.post("/picture/{picture_path:path}")
def take_path(picture_path: str):
    return invert_picture(picture_path)


def invert_picture(path):
    img = Image.open(path)
    invert_img = ImageChops.invert(img)
    invert_img.show()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"mtomanek"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"haslo"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/time")
def read_user(username: str = Depends(get_current_username)):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    return {time}
