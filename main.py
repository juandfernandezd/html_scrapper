from fastapi import FastAPI
from pydantic import BaseModel
from scraper import Scrapper
from typing import List

app = FastAPI()


class URLInput(BaseModel):
    url: str

class URLSearchInput(BaseModel):
    url: str
    search: List[str]

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

    results = {}
    for search_term in search_input.search:
        result = scrapper.find_element_path(tree, search_term)
        results.update({search_term: result})
    scrapper.close()
    return results
