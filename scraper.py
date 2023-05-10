from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


class Scrapper:

    def __init__(self, url):

        self.url = url
        self.driver = self.prepare_site()
        self.body = self.get_source_code()

    def prepare_site(self, *, headless: bool = True):
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

        driver.get(self.url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        return driver

    def get_source_code(self) -> BeautifulSoup:
        src = self.driver.page_source
        soup = BeautifulSoup(src, 'html.parser')
        return soup.body

    def add_child_nodes(self, body, node):
        for child in body.children:
            if child.name is not None:
                child_node = {
                    'name': child.name,
                    'attrs': child.attrs,
                    'children': []
                }
                node['children'].append(child_node)
                self.add_child_nodes(child, child_node)

    def get_tree(self):
        root_node = {
            'name': self.body.name,
            'attrs': self.body.attrs,
            'children': []
        }

        self.add_child_nodes(self.body, root_node)

        return root_node

    def close(self):
        self.driver.close()
