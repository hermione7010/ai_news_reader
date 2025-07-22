import requests
from bs4 import BeautifulSoup
import re

# RSS feed URL
rss_url = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"

# Output file
output_file = "scraped_news.txt"

def extract_article_urls_from_rss(rss_url):
    response = requests.get(rss_url)
    soup = BeautifulSoup(response.content, "xml")

    article_urls = []
    for item in soup.find_all("item"):
        description = item.find("description").text
        # Find href in <a href="...">
        match = re.search(r'href="([^"]+)"', description)
        if match:
            article_urls.append(match.group(1))
    return article_urls

def scrape_article_content(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")
        
        # Times of India usually wraps article content in div with class="ga-headlines"
        content_divs = soup.find_all("div", class_=re.compile(".*article.*|.*ga-headlines.*"))
        content = []

        for div in content_divs:
            for p in div.find_all("p"):
                text = p.get_text(strip=True)
                if text:
                    content.append(text)
        
        return "\n".join(content) if content else "No article text found."
    except Exception as e:
        return f"Failed to retrieve article: {e}"

def main():
    urls = extract_article_urls_from_rss(rss_url)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for i, url in enumerate(urls):
            print(f"Scraping ({i+1}/{len(urls)}): {url}")
            content = scrape_article_content(url)
            f.write(f"--- Article {i+1} ---\n{content}\n\n")

if __name__ == "__main__":
    main()
