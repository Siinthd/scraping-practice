import easyocr

def text_extract(filename):
    reader = easyocr.Reader(['ru'])
    result = reader.readtext(filename)
    return result
