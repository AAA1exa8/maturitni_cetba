import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


BASE_URL = "https://rozbor-dila.cz/"
cached_list: dict[str, str] = {}

def get_urls_for_book(name: str) -> dict[str, str]:
    if len(cached_list) == 0:
        print("Fetching URLs...")
        response = requests.get(BASE_URL + "seznam-rozboru-ramec/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table_links = soup.select('.table-link')
        for link in table_links:
            href = link.get('href')
            if href:
                cached_list[link.text.strip()] = str(href).replace(BASE_URL, "")
    urls = {}
    for book_name, url in cached_list.items():
        if name.lower() in book_name.lower():
            urls[book_name] = url
    return urls



def get_md_for_book(url: str) ->  str:
    response = requests.get(BASE_URL + url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    inside_article = soup.find('div', class_='inside-article')
    if inside_article:
        for tag in inside_article.select('.ai-viewports'):
            tag.decompose()  

        
        return md(str(inside_article))

    else:
        raise ValueError("No div with class 'inside-article' found.")

