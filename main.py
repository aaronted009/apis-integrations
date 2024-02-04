from fastapi import FastAPI, Form, Request, Response
from fastapi.templating import Jinja2Templates
import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

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


@app.get("/news-top-headlines/")
async def news_top_headlines(request: Request) -> Response:
    """News top headlines api call."""

    url = "https://news-api14.p.rapidapi.com/top-headlines"

    querystring = {
        "country": "us",
        "language": "en",
        "pageSize": "10",
        "category": "sports",
    }

    headers = {
        "X-RapidAPI-Key": os.getenv("NEWS-API-KEY"),
        "X-RapidAPI-Host": "news-api14.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    return templates.TemplateResponse(
        "news-top-headlines.jinja", {"request": request, "response": response.json()}
    )


@app.get("/search-form/")
async def search_form(request: Request) -> Response:
    """News api search form."""

    return templates.TemplateResponse("search-form.jinja", {"request": request})


@app.post("/search-form/")
async def search_news(
    request: Request,
    search_query: str = Form(),
) -> Response:
    """News api search news page."""

    url = "https://news-api14.p.rapidapi.com/search"

    querystring = {
        "q": search_query,
        "country": "us",
        "language": "en",
        "pageSize": "10",
        "publisher": "cnn.com,bbc.com",
    }

    headers = {
        "X-RapidAPI-Key": os.getenv("NEWS-API-KEY"),
        "X-RapidAPI-Host": "news-api14.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
    return templates.TemplateResponse(
        "search-news.jinja", {"request": request, "response": response.json()}
    )


@app.get("/chatgpt/")
async def chatgpt(request: Request) -> Response:
    """ChatGPT api page."""
    return templates.TemplateResponse("gpt-api.jinja", {"request": request})


@app.post("/chatgpt/")
async def chatgpt_results(
    request: Request,
    gpt_query: str = Form(),
) -> Response:
    """ChatGPT api page."""
    openai.api_key = os.getenv("OPENAI-API-KEY")
    messages=[{"role": "system", "content": "You are a helpful assistant."}]
    if gpt_query:
        messages.append(
            {"role": "user", "content": gpt_query},
        )
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
        except Exception as e:
            print("Exception : ", e)
    reply = completion.choices[0].message.content if completion else "No answer from ChatGPT; please check your logs."
    return templates.TemplateResponse(
        "gpt-api-results.jinja", {"request": request, "query": gpt_query, "reply": reply}
    )
