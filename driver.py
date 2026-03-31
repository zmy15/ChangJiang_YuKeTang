from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


def configure_driver(config):
    edge_options = Options()
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_driver_path = config.edge_driver_path
    service = Service(edge_driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    return driver


class driver:
    def __init__(self, config):
        self.driver = configure_driver(config)
