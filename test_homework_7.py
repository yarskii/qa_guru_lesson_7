import os.path
import time
from pypdf import PdfReader
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from zipfile import ZipFile

from script_os import TMP_DIR, NUM


def test_downloading_file(open_browser):
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

    with ZipFile(f'{TMP_DIR}/zzip.zip', 'w') as my_zip_file:
        my_zip_file.write(f'{TMP_DIR}/sample-{NUM}.pdf', arcname=f'sample-{NUM}.pdf')
        my_zip_file.close()

    with ZipFile(f'{TMP_DIR}/zzip.zip') as a:
        with a.open(f'sample-{NUM}.pdf') as pdf:
            reader = PdfReader(pdf)
            page = reader.pages[0]
            print(page.extract_text())
