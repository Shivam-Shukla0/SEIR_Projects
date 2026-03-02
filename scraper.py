import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrape_page(website_link):
    if not website_link.startswith("http") and not website_link.startswith("https"):
        website_link = "https://" + website_link

    op = Options()
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=op)
    driver.get(website_link)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    filter_html_page = BeautifulSoup(html, "html.parser")

    if filter_html_page.title and filter_html_page.title.string:
        print(filter_html_page.title.string.strip())
    else:
        print("")

    elements = filter_html_page(["script", "style"])
    while len(elements) > 0:
        elements[0].decompose()
        elements = filter_html_page(["script", "style"])

    body_tag_content = filter_html_page.find("body")
    if body_tag_content:
        text_data = body_tag_content.get_text(separator="\n")
        lines = text_data.split("\n")
        i = 0
        while i < len(lines):
            cleaned_content = lines[i].strip()
            if cleaned_content:
                print(cleaned_content)
            i += 1

    links = filter_html_page.find_all("a", href=True)
    i = 0
    while i < len(links):
        print(urljoin(website_link, links[i]["href"]))
        i += 1

if __name__ == "__main__":
    if len(sys.argv) == 2:
        scrape_page(sys.argv[1])