import pyttsx3
import pdfplumber
import PyPDF2
import os

CURRENTFOLDER = os.path.dirname(__file__)
books_path = os.path.join(CURRENTFOLDER,'Books')
audios_path = os.path.join(CURRENTFOLDER,'Generated Books') 

os.makedirs( books_path, exist_ok=True)
os.makedirs( audios_path, exist_ok=True)

def readPages(pdf_path, title, initial_page, final_page, generation_path):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    # Read the file
    content = ""
    for i in range(initial_page, final_page):
        with pdfplumber.open(pdf_path) as temp:
            text = temp.pages[i]
            content = content + text.extract_text()
        # Control the rate. Higher rate = more speed
    title = title.replace(".pdf", "")    
    output_file = f"{title} {initial_page}-{final_page}.mp3"
    audio = content.replace ("\n", "")
    print(audio)
    if(audio==''):
        audio='No hay contenido para leer en esta página'
    output_path = os.path.join(generation_path, output_file)
    print(output_path)
    engine.save_to_file(audio, output_path)
    engine.runAndWait()

def convert_book(pdf_path, name, page, total_pages, generation_path):
    if(page<total_pages):
        readPages(pdf_path, name, page, page+1, generation_path)
    else:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        
        audio = 'Usted ha concluido el contenido'
        root_path = os.path.dirname(os.path.dirname(pdf_path))
        output_file = f"{name} {page}-{page+1}.mp3"
        output_path = os.path.join(generation_path, output_file)
        engine.save_to_file(audio, output_path)
        engine.runAndWait()

files = os.listdir(os.path.join(CURRENTFOLDER,'Books'))

for file_name in files:
    file_path = os.path.join(books_path, file_name)
    print(file_path)
    file = open(file_path, 'rb')
    readpdf = PyPDF2.PdfFileReader(file)
    total_pages = readpdf.numPages
    print("Filename: "+ file_name)
    print("Total Pages: "+str(total_pages))
    print("_______________________________")
    for page in range(total_pages):
        convert_book(file_path, file_name, page, total_pages, audios_path)