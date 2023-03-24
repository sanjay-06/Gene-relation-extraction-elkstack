from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from elasticsearch_config.elasticsearch_index import EsManagement
from fastapi.responses import RedirectResponse

search = APIRouter()
templates=Jinja2Templates(directory="static")

@search.get('/')
def return_html(request : Request):
    return templates.TemplateResponse("index.html",{"request":request})

@search.post('/submit')
async def handle_submit(request: Request, search: str = Form(...)):
    search_array = search.split(" ")
    print(search_array)
    es = EsManagement()
    url = es.search(search_array)
    return RedirectResponse(url)
    

    