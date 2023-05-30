from fastapi import FastAPI, UploadFile, File, Request, Form
import uvicorn
from program.person_detection import read_image
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List


app = FastAPI()
IMAGEDIR = "images/"
app.mount("/images", StaticFiles(directory="images", html=True), name="images")
templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post('/count')
async def count(files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        # save the file
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)
    text = [read_image(f"{IMAGEDIR}{file.filename}") for file in files]
    return {"Result": "OK", "Text": text}




@app.post("/upload-files")
async def create_upload_files(request: Request, files: List[UploadFile] = File(...)):
    for file in files:
        contents = await file.read()
        # save the file
        with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
            f.write(contents)

    show = [file.filename for file in files]
    text = [read_image(f"{IMAGEDIR}{file.filename}") for file in files]

    # return {"Result": "OK", "filenames": [file.filename for file in files]}
    return templates.TemplateResponse("index.html", {"request": request, "show": show, "text": text})



@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, port = 5000)