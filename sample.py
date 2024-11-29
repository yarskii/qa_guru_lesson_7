from zipfile import ZipFile
from pypdf import PdfReader
from script_os import TMP_DIR


with ZipFile(f'{TMP_DIR}/zzip.zip', 'w') as my_zip_file:
    my_zip_file.write(f'{TMP_DIR}/sample-5.pdf', arcname='sample.pdf')
    my_zip_file.close()


with ZipFile(f'{TMP_DIR}/zzip.zip') as a:
    with a.open('sample.pdf') as pdf:
        reader = PdfReader(pdf)
        page = reader.pages[0]
        print(page.extract_text())
