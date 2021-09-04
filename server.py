import asyncio
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import Response


app = FastAPI()


@app.get("/")
def index_page():
    """Рендер главной страницы"""
    with open('templates/index.html', 'r') as f:
        index_page = f.read()
    return Response(index_page, media_type='text/html')



@app.post("/read")
async def create_file(input_file: UploadFile = File(...)):
    """"""
    file_content = await input_file.read()
    print(file_content)
    response = {
        "file_size": len(input_file),
        "fileb_content_type": input_file.content_type,
    }
    print("Responce:", response)
    