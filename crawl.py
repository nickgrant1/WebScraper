from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
        

def normalize_url(url):
    o = urlparse(url)
    result=''
    if o.netloc:
        result += o.netloc.lower()
    if o.path:
        result += o.path.lower()
    return result.rstrip('/')


def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    header = soup.find('h1')
    if header:
        return header.get_text()
    return ''

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find('main')
    if main:
        paragraphs = main.find_all('p')
        for p in paragraphs:
            if p.get_text():
                return p.get_text()
    
    paragraphs = soup.find_all('p')
    for p in paragraphs:
        if p.get_text():
            return p.get_text()
    return ''

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        links = [urljoin(base_url, a['href']) for a in soup.find_all('a')]
        return links
    except Exception as e:
        return e

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        if not img.get('src'):
            raise KeyError('Image is missing an attribute')
    try:
        imgs = [urljoin(base_url, i['src']) for i in soup.find_all('img')] 
        return imgs
    except Exception as e:
        return e

def extract_page_data(html, page_url):
    d = {'page_url': page_url}
    d['h1'] = get_h1_from_html(html)
    d['first_paragraph'] = get_first_paragraph_from_html(html)
    d['outgoing_link_urls'] = get_urls_from_html(html, page_url)
    d['image_urls'] = get_images_from_html(html, page_url)
    return d
