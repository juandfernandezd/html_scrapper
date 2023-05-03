import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


BASE_URL = f'https://www.linkedin.com/signup/cold-join?source=guest_homepage-basic_nav-header-signin'


def prepare_site(*, headless: bool=True):
    options = Options()
    options.add_argument('window-size=1400,900')
    if headless:
        options.add_argument('headless')

    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    driver.get(BASE_URL)
    time.sleep(3)
    return driver


def get_source_code() -> BeautifulSoup:
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
    print(soup.body.prettify)
    return soup.body


def add_child_nodes(body, node):
    for child in body.children:
        if child.name is not None:
            child_node = {
                'name': child.name,
                'attrs': child.attrs,
                'children': []
            }
            node['children'].append(child_node)
        

if __name__ == '__main__':
    driver = prepare_site(headless=False)
    soup = get_source_code()
    tree = {}
    root_node = {
        'name': soup.name,
        'attrs': soup.attrs,
        'children': []
    }
    tree['root'] = root_node

    add_child_nodes(soup, root_node)
    print('-' * 100)
    print(tree)
    print('-' * 100)
    driver.close()
