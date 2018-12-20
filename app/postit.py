import io
import sys

from google.cloud import vision_v1p3beta1 as vision
import requests

from settings import GITHUB_OAUTH_TOKEN, ISSUES_URL


def get_open_issues():
    headers = {
        'Authorization': f'token {GITHUB_OAUTH_TOKEN}'
    }

    issue_list = requests.get(ISSUES_URL, headers=headers)
    print(issue_list.json())
    issues = [
        issue['number']
        for issue in issue_list.json()
    ]
    return issues

def close_issues(issues):
    headers = {
        'Authorization': f'token {GITHUB_OAUTH_TOKEN}'
    }

    for issue_number in issues:
        issue_url = f'{ISSUES_URL}/{issue_number}'
        params = {'state': 'closed'}
        requests.patch(issue_url, headers=headers, json=params)

def get_issues_from_ocr(ocr_text):
    tokens = ocr_text.split('\n')

    board_column = tokens[0]
    column_cards = [int(token[1:]) for token in tokens if token and '#' in token[0]]
    return column_cards

def detect_handwritten_ocr(path):
    """Detects handwritten characters in a local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    # Language hint codes for handwritten OCR:
    # en-t-i0-handwrit, mul-Latn-t-i0-handwrit
    # Note: Use only one language hint code per request for handwritten OCR.
    image_context = vision.types.ImageContext(
        language_hints=['en-t-i0-handwrit'])

    response = client.document_text_detection(image=image,
                                              image_context=image_context)
    
    return response.full_text_annotation.text

def get_issues_to_close(candidate_issues, open_issues):
    return [issue for issue in candidate_issues if issue in open_issues]

def sync_board(path):
    ocr_text = detect_handwritten_ocr(path)
    print(ocr_text)

    img_issues = get_issues_from_ocr(ocr_text)
    print(img_issues)

    open_issues = get_open_issues()
    print(open_issues)

    issues_to_close = get_issues_to_close(img_issues, open_issues)
    print(issues_to_close)

    close_issues(issues_to_close)

    return issues_to_close

