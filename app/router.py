from utils import open_image, ocr

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def classify_image(img_path):
    img = open_image(img_path)
    ocr_text = ocr(img)

    if 'mosaicscience' in ocr_text:
        return 'mosaic'
    
    days_mentioned = [token for line in ocr_text.split('\n') for token in line.split(' ') if token in DAYS]
    if len(days_mentioned) > 5:
        return 'food'

    return 'trustnet'
