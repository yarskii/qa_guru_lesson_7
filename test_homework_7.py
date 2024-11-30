from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from zipfile import ZipFile
from openpyxl import load_workbook
from pypdf import PdfReader
import os.path
import shutil
import time
import csv
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

    with ZipFile('zzip.zip', 'w') as zip_f:

        for file in os.listdir(TMP_DIR):
            add_file = os.path.join(TMP_DIR, file)
            zip_f.write(add_file, arcname=file)

    with ZipFile('zzip.zip') as zip_file:
        for file in zip_file.namelist():

            if file.split('.')[-1] == 'pdf':
                with zip_file.open(file) as pdf_file:
                    reader = PdfReader(pdf_file)
                    text_pdf = ''
                    for page in reader.pages:
                        text_pdf += f'{page.extract_text()} \n'

                assert text_pdf is not None, f"Не удалось извлечь текст из страницы PDF {file}"
                assert len(reader.pages) > 0, f"PDF файл {file} пуст!"

            elif file.split('.')[-1] == 'csv':
                with zip_file.open(file) as csv_file:
                    content = csv_file.read().decode('utf-8-sig')
                    csvreader = list(csv.reader(content.splitlines()))
                    text_csv = ''
                    for line in csvreader:
                        text_csv += f'{line} \n'

                assert text_csv is not None, f"CSV файл {file} пуст!"

            elif file.split('.')[-1] == 'xlsx':
                with zip_file.open(file) as xlsx_file:
                    workbook = load_workbook(xlsx_file)
                    sheet = workbook.active
                    text_xlsx = ''
                    for row in sheet.iter_rows():
                        for cell in row:
                            if cell.value is None:
                                continue
                            text_xlsx += f'{cell.value} \n'

                assert text_xlsx is not None, f"XLSX файл {file} пуст!"

    assert len(zip_file.namelist()) > 0
    assert os.path.isfile('zzip.zip')

    os.remove('zzip.zip')
    shutil.rmtree(TMP_DIR)

    assert not os.path.isfile('zzip.zip')
    assert not os.path.isdir(TMP_DIR)
