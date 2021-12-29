import pytesseract as tess
# to add it to the environment variable the tesseract CR
tess.pytesseract.tesseract_cmd = r'C:\\Users\\rmastour\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
from PIL import Image

img = Image.open('test.jpg')
text = tess.image_to_string(img)

print(text)
