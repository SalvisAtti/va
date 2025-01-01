# Updated main.py
from fastapi import FastAPI
from pydantic import BaseModel
from MainVA import play_on_youtube, tell_time, tell_date, provide_greeting, tell_name, search_wikipedia, calculate

app = FastAPI()

class YouTubeQuery(BaseModel):
    query: str

class WikipediaQuery(BaseModel):
    query: str

class CalculationQuery(BaseModel):
    expression: str

@app.post("/play-youtube/")
async def play_youtube(video: YouTubeQuery):
    result = play_on_youtube(video.query)
    return {"response": result}

@app.get("/time/")
async def get_time():
    return {"time": tell_time()}

@app.get("/date/")
async def get_date():
    return {"date": tell_date()}

@app.get("/greeting/")
async def greeting():
    return {"greeting": provide_greeting()}

@app.get("/name/")
async def name():
    return {"name": tell_name()}

@app.post("/search-wikipedia/")
async def search_wiki(wiki_query: WikipediaQuery):
    result = search_wikipedia(wiki_query.query)
    return {"response": result}

@app.post("/calculate/")
async def calc(query: CalculationQuery):
    result = calculate(query.expression)
    return {"result": result}
