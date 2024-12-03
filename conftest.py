import os
import shutil
import time
from zipfile import ZipFile

from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest

from script_os import TMP_DIR, NUM


@pytest.fixture(scope='session')
def open_browser():
    driver_options = webdriver.ChromeOptions()
    driver_options.page_load_strategy = 'eager'
    browser.config.driver_options = driver_options
    browser.config.base_url = 'https://getsamplefiles.com'
    browser.config.headless = True
    browser.config.window_width = 1280
    browser.config.window_height = 720

    yield

    browser.quit()


@pytest.fixture(scope='session')
def downloading_file(open_browser):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": TMP_DIR,
        "download.prompt_for_download": False
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.config.driver = driver

    browser.open(f'/download/pdf/sample-{NUM}.pdf')
    time.sleep(1)
    browser.open(f'/download/xlsx/sample-{NUM}.xlsx')
    time.sleep(1)
    browser.open(f'/download/csv/sample-{NUM}.csv')
    time.sleep(1)

    yield

    driver.quit()


@pytest.fixture(scope='session')
def create_zip(downloading_file):
    with ZipFile('zzip.zip', 'w') as zip_f:
        for file in os.listdir(TMP_DIR):
            add_file = os.path.join(TMP_DIR, file)
            zip_f.write(add_file, arcname=file)

    yield

    if os.path.exists('zzip.zip'):
        os.remove('zzip.zip')

    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR)

    print('Temporary files have been deleted')
