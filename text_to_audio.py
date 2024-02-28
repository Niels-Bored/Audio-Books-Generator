import pyttsx3
import pdfplumber
import PyPDF2
import os

CURRENTFOLDER = os.path.dirname(__file__)

engine = pyttsx3.init()
engine.setProperty("rate", 150)

def readPages(pdf_path, title, initial_page, final_page):
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
    output_path = os.path.join(CURRENTFOLDER, 'Generated Books', output_file)
    print(output_path)
    engine.save_to_file(audio, output_path)
    engine.runAndWait()

def convert_book(pdf_path, name, page, total_pages):
    

    if(page<total_pages):
        readPages(pdf_path, name, page, page+1)
    else:
        audio = 'Usted ha concluido el contenido'
        root_path = os.path.dirname(os.path.dirname(pdf_path))
        output_file = f"{name} {page}-{page+1}.mp3"
        output_path = os.path.join(root_path, 'Generated Books', output_file)
        engine.save_to_file(audio, output_path)
        engine.runAndWait()


filename = 'Dracula.pdf'
file_path = os.path.join(CURRENTFOLDER,'Books', filename)
print(file_path)
file = open(file_path, 'rb')
readpdf = PyPDF2.PdfFileReader(file)
total_pages = readpdf.numPages
print("Filename: "+ filename)
print("Total Pages: "+str(total_pages))
print("_______________________________")
for page in total_pages:
    convert_book(file_path, filename, page, total_pages)