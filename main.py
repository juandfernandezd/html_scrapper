from fastapi import FastAPI
from pydantic import BaseModel
from scraper import Scrapper

app = FastAPI()


class URLInput(BaseModel):
    url: str


@app.post("/")
async def show_url_tree(url_input: URLInput):
    scrapper = Scrapper(url_input.url)
    tree = scrapper.get_tree()
    scrapper.close()
    return tree
