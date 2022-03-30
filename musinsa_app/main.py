from fastapi import FastAPI
from typing import Optional
import musinsa


app = FastAPI()


@app.get("/")
@app.get("/{old_target}")
def home(old_target: Optional[int] = 0):
    user_names = musinsa.getUserList()
    access_key_list = musinsa.getAccessKeys(user_names)
    access_key_list = musinsa.appendHowOld(access_key_list, old_target)
    return {"access_key_list": access_key_list}
