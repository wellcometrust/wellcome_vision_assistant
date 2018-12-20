from bs4 import BeautifulSoup
import requests

from utils import open_image, ocr


def clean_title(text):
    if type(text)=='byte':
        text = text.decode('ascii', 'ignore')
    text = text.replace('\n', ' ')
    text = text.encode('ascii', 'ignore')
    return text

def read_title(img):
    ocr_text = ocr(img)
    ocr_title = ocr_text.split('\n\n')[0]
    return ocr_title

def get_google_first_result(query):
    google_url = 'https://www.google.co.uk/search'
    mosaic_url = 'https://mosaicscience.com/'
    params = {
        'q': f"site:{mosaic_url} {query}"
    }
    print(params)
    response = requests.get(google_url, params=params)

    soup = BeautifulSoup(response.text, 'html.parser')
    first_result = soup.find('h3', {'class': 'r'})

    result_url = None
    if first_result:
        result_url = first_result.a['href'].split('/url?q=')[1].split('&')[0]
    return result_url

def get_mosaic_first_result(query):
    pass

def get_mosaic_title(mosaic_article_url):
    response = requests.get(mosaic_article_url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    return soup.find('title').text

def calculate_title_similarity(first_title, second_title):
    first_title = clean_title(first_title)
    second_title = clean_title(second_title)
    
    first_title_words = first_title.split()
    second_title_words = second_title.split()

    nb_unique_words = len(set(first_title_words).union(set(second_title_words)))
    nb_common_words = len(set(first_title_words).intersection(set(second_title_words)))

    return nb_common_words/nb_unique_words

def find_mosaic_url(img=None, img_path=None):
    if img_path:
        img = open_image(img_path)

    img_title = read_title(img)
    print(img_title)
    mosaic_url = get_google_first_result(img_title)
    print(mosaic_url)

    if mosaic_url:
        mosaic_title = get_mosaic_title(mosaic_url)
        print(mosaic_title)

        similarity_score = calculate_title_similarity(mosaic_title, img_title)
        print(similarity_score)

        if similarity_score < 0.2:
            return "https://s3-us-west-2.amazonaws.com/hs-production-blog/blog/wp-content/uploads/2017/01/27124612/headspace_blog_wrong.gif"

        return mosaic_url

    return "https://cdn.dribbble.com/users/1554526/screenshots/3399669/no_results_found.png"
