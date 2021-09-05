import codecs
import re
from fastapi import FastAPI, File, UploadFile
from fastapi.templating import Jinja2Templates


TEMPLATES = Jinja2Templates(directory='templates')
app = FastAPI()


@app.get("/")
def index_page():
    """Рендер главной страницы"""
    return TEMPLATES.TemplateResponse('index.html') 


@app.post("/read")
async def read_file(input_file: UploadFile = File(...)):
    """Принимает файл из формы и читает его."""

    file_content = await input_file.read()
    file_content = codecs.decode(file_content, encoding='utf-8', errors='replace')
    return {"Word":"TF"}, file_parse(file_content)

    

def file_parse(file: str):
    """Формирует список 50 самых частых слов в тексте."""
    input_string = ' '.join(file.split()).replace('\n', '').lower()
    data = re.sub(r'[^\w\s]', '', input_string)
    data = re.sub(r'\s\w{1,2}\s', ' ', data).split(" ")   

    divider = len(data)
    reference = sorted(list(set(data)))

    # Считаем словом всё, что не меньше 2 символов.
    for word in reference:
        if len(word) < 2:
            reference.remove(word)

    dic = {}
    for word in reference:
        tf = data.count(word)/divider
        if tf not in dic.keys():
            dic[tf] = []
            dic[tf].append(word)
        else:
            dic[tf].append(word)

    sorted_dic = {}
    for i in sorted(dic.keys(), reverse=True):
        sorted_dic[i] = dic[i]
    del(dic)

    result = {}
    for i in sorted_dic.keys():
        for j in sorted_dic[i]:
            result[str(j)] = str(i)

    return result

    