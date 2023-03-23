from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

search = APIRouter()
templates=Jinja2Templates(directory="static")

@search.get('/')
def return_html(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})

@search.post('/submit')
async def handle_submit(request: Request, search: str = Form(...)):
    print(search)

    