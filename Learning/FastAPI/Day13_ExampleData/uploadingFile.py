from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI() 

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile")
async def create_upload_file(file: UploadFile):
    file_name = {"filename": file.filename}
    contents = await file.seek(0)
    print(contents)
    return file_name