from selene import browser
from selenium import webdriver
import pytest


@pytest.fixture(scope='session')
def open_browser():
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options
    browser.config.base_url = 'https://getsamplefiles.com'
    browser.config.headless = True
    browser.config.window_width = 1280
    browser.config.window_height = 720
