from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request) -> Response:
    """Home page."""
    return templates.TemplateResponse("home.jinja", {"request": request})

@app.get("/news/")
async def news(request: Request) -> Response:
    """News api page."""
    return templates.TemplateResponse("news-api.jinja", {"request": request})

@app.get("/chatgpt/")
async def chatgpt(request: Request) -> Response:
    """ChatGPT api page."""
    return templates.TemplateResponse("gpt-api.jinja", {"request": request})