# uvicorn main:app --host=0.0.0.0 --port=8000 --reload
from fastapi import FastAPI
from fastapi.responses import FileResponse
import musinsa

app = FastAPI()


@app.get("/")
@app.get("/{old_target}")
def home(old_target: int = 0):
    print(old_target)
    iam = musinsa.loadCredential()
    user_names = musinsa.getUserList(iam)
    access_key_list = musinsa.getAccessKeys(iam, user_names)
    access_key_list = musinsa.appendHowOld(access_key_list, old_target)
    make_file_result = musinsa.makeCSV(access_key_list)
    print(make_file_result)
    return FileResponse(path="AccessKeyList.csv", filename="AccessKeyList.csv")
    # return {"access_key_list": access_key_list} # if you want to return JSON
