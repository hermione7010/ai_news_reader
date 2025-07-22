import requests
from bs4 import BeautifulSoup
import re
import os
import hashlib

# RSS feed URL
rss_url = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"

# Output directory
output_dir = "scraped_news"
os.makedirs(output_dir, exist_ok=True)

def extract_article_urls_from_rss(rss_url):
    response = requests.get(rss_url)
    soup = BeautifulSoup(response.content, "xml")

    article_urls = []
    for item in soup.find_all("item"):
        description = item.find("description").text
        match = re.search(r'href="([^"]+)"', description)
        if match:
            article_urls.append((item.title.text, match.group(1)))  # Return title + URL
    return article_urls

def clean_filename(name):
    # Remove invalid characters for filenames and truncate long titles
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip()[:100]  # Limit filename length
def nothing():
# def scrape_article_content(url):
#     try:
#         page = requests.get(url, timeout=10)
#         soup = BeautifulSoup(page.content, "html.parser")

#         # Extract title
#         title_tag = soup.find("h1", class_="HNMDR")
#         title = title_tag.get_text(strip=True) if title_tag else "No title found"

#         # Main content div
#         content_div = soup.find("div", class_="_s30J clearfix")
#         if not content_div:
#             content_divs = soup.find_all("div", attrs={"data-type": "in_view"})
#         else:
#             content_divs = [content_div]

#         paragraphs = []

#         for div in content_divs:
#             # Standard paragraph tags
#             for tag in div.find_all(["p", "div", "span", "section"], recursive=True):
#                 text = tag.get_text(strip=True)
#                 if text:
#                     paragraphs.append(text)

#             # Also get text immediately following span.id-r-component.br
#             for span in div.find_all("span", class_="id-r-component br"):
#                 next_text = span.next_sibling
#                 print(next_text)
#                 if isinstance(next_text, str):
#                     clean = next_text.strip()
#                     if clean:
#                         paragraphs.append(clean)

#         article_text = "\n".join(paragraphs).strip()
#         if not article_text:
#             article_text = "No article text found."

#         return f"{title}\n\n{article_text}"

#     except Exception as e:
#         return f"Failed to retrieve article: {e}"


# def scrape_article_content(url):
#     try:
#         page = requests.get(url, timeout=10)
#         soup = BeautifulSoup(page.content, "html.parser")

#         # Extract headline
#         title_tag = soup.find("h1", class_="HNMDR")
#         title = title_tag.get_text(strip=True) if title_tag else "No title found"

#         # Find main article body container
#         main_body = soup.find("div", attrs={"data-articlebody": "1"})
#         if not main_body:
#             return f"{title}\n\nNo article content found."

#         paragraphs = []

#         # Extract visible text from relevant tags
#         for tag in main_body.find_all(["div", "span", "p"], recursive=True):
#             # Clean direct tag text
#             text = tag.get_text(strip=True)
#             if text:
#                 paragraphs.append(text)

#         # Also grab text directly following <span class="id-r-component br">
#         for span in main_body.find_all("span", class_="id-r-component br"):
#             next_text = span.next_sibling
#             if isinstance(next_text, str):
#                 clean = next_text.strip()
#                 if clean:
#                     paragraphs.append(clean)

#         article_text = "\n".join(paragraphs).strip()
#         if not article_text:
#             article_text = "No article text found."

#         return f"{title}\n\n{article_text}"

#     except Exception as e:
#         return f"Failed to retrieve article: {e}"

    pass

def scrape_article_content(url):
    try:
        print("#"*170)
        print(f"Scraping article: {url}")
        print("#"*170)
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.content, "html.parser")

        # Extract headline
        title_tag = soup.find("h1", class_="HNMDR")
        title = title_tag.get_text(strip=True) if title_tag else "No title found"

        # Find main article content
        article_div = soup.find("div", attrs={"data-articlebody": "1"})
        if not article_div:
            return f"{title}\n\nNo article content found."

        # Just get all the raw text inside the main article div
        content = article_div.get_text(separator="\n", strip=True)

        return f"{title}\n\n{content}"

    except Exception as e:
        return f"Failed to retrieve article: {e}"




def main():
    articles = extract_article_urls_from_rss(rss_url)

    for i, (title, url) in enumerate(articles):
        print(f"Scraping ({i+1}/{len(articles)}): {title}")
        content = scrape_article_content(url)

        filename = clean_filename(title)
        if not filename:
            filename = hashlib.md5(url.encode()).hexdigest()
        filepath = os.path.join(output_dir, f"{filename}.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{title}\n{url}\n\n{content}")

if __name__ == "__main__":
    main()
