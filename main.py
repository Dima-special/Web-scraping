import requests
import bs4

KEYWORDS = ['дизайн', 'фото', 'web', 'python']

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.4.727 Yowser/2.5 Safari/537.36'
}

url = 'https://habr.com/ru/all/'

response = requests.get(url, headers=HEADERS)
response.raise_for_status()

soup = bs4.BeautifulSoup(response.text, features='html.parser')
articles = soup.find_all('article', class_='tm-articles-list__item')

if not articles:
    print("Статьи не найдены. Проверьте структуру HTML.")
else:
    print(f"Найдено {len(articles)} статей.")

matching_articles = []

for article in articles:
    date = article.find('time').text
    title_element = article.find('a', class_='tm-article-snippet__title-link')
    
    if title_element:
        title = title_element.text.strip()
        href = title_element['href']
        url = 'https://habr.com' + href

        preview_text = article.find('div', class_='tm-article-snippet__lead').text if article.find('div', class_='tm-article-snippet__lead') else ''
        full_text = title + ' ' + preview_text

        if any(keyword.lower() in full_text.lower() for keyword in KEYWORDS):
            matching_articles.append(f"{date} – {title} – {url}")

if matching_articles:
    for article in matching_articles:
        print(article)
else:
    print("Подходящие статьи не найдены.")
