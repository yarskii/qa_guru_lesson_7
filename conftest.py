import os
import shutil
from zipfile import ZipFile

from selene import browser
from selenium import webdriver
import pytest

from script_os import TMP_DIR


@pytest.fixture(scope='session', autouse=True)
def open_browser():
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options
    browser.config.base_url = 'https://getsamplefiles.com'
    browser.config.headless = True
    browser.config.window_width = 1280
    browser.config.window_height = 720


@pytest.fixture
def create_zip():
    with ZipFile('zzip.zip', 'w') as zip_f:
        for file in os.listdir(TMP_DIR):
            add_file = os.path.join(TMP_DIR, file)
            zip_f.write(add_file, arcname=file)


@pytest.fixture
def del_elements():
    os.remove('zzip.zip')
    shutil.rmtree(TMP_DIR)
