from fastapi import FastAPI
from pydantic import BaseModel
from scraper import Scrapper

app = FastAPI()


class URLInput(BaseModel):
    url: str

class URLSearchInput(BaseModel):
    url: str
    search: str

@app.post("/tree")
async def show_url_tree(url_input: URLInput):
    scrapper = Scrapper(url_input.url)
    tree = scrapper.get_tree()
    scrapper.close()
    return tree

@app.post("/search")
async def search_selector_in_tree(search_input: URLSearchInput):
    scrapper = Scrapper(search_input.url)
    tree = scrapper.get_tree()
    result = scrapper.find_element_path(tree, search_input.search)
    scrapper.close()
    return result
