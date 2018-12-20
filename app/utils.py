try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract

def open_image(img_path):
    img=Image.open(img_path)
    img = img.rotate(-90, expand=True)
    return img

def ocr(img):
	return pytesseract.image_to_string(img)
