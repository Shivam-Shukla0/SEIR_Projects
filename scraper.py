import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def scrape_page(website_link):
    if not website_link.startswith("http") and not website_link.startswith("https"):
        website_link = "https://" + website_link

    # browser silently chalao
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(website_link)

    # JS load hone ka wait karo
    time.sleep(3)

    html = driver.page_source
    driver.quit()

    filter_html_page = BeautifulSoup(html, "html.parser")

    # title
    if filter_html_page.title and filter_html_page.title.string:
        print(filter_html_page.title.string.strip())
    else:
        print("")

    # script style hatao
    elements = filter_html_page(["script", "style"])
    while len(elements) > 0:
        elements[0].decompose()
        elements = filter_html_page(["script", "style"])

    # body text
    body_tag_content = filter_html_page.find("body")
    if body_tag_content:
        text = body_tag_content.get_text()
        lines = text.split("\n")
        i = 0
        while i < len(lines):
            cleaned_content = lines[i].strip()
            if cleaned_content:
                print(cleaned_content)
            i += 1

    # links
    for anchor_tag_in_page in filter_html_page.find_all("a", href=True):
        print(urljoin(website_link, anchor_tag_in_page["href"]))


if __name__ == "__main__":
    if len(sys.argv) == 2:
        scrape_page(sys.argv[1])