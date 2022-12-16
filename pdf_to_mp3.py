from gtts import gTTS
import pdfplumber
from art import tprint
from pathlib import Path

def pdf_mpe(filepath,lang):

    if Path(filepath).is_file() and Path(filepath).suffix == '.pdf':
        with pdfplumber.PDF(open(file=filepath,mode='rb')) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
        print('text extracted')
        text=''.join(pages)
        text=text.replace('\n',' ')
        audio = gTTS(text=text,lang=lang,slow=False,)
        filename = Path(filepath).stem
        audio.save(f'data_capture/{filename}.mp3')
        tprint(f'filename {filename}.mp3 saved',font='bulbhead')
    else:
        print('?')

if __name__ == "__main__":
    pdf_mpe(r"C:\Users\DevSiinthd\Downloads\Sample.pdf",'en')
