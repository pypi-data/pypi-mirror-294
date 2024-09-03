import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_community.document_loaders import BSHTMLLoader
from pydantic import BaseModel


class SearchResult(BaseModel):
    title_and_links: list = []
    google_top_response: str = ""
    html_content: str = ""
    urls: list = []


class GoogleSearcher:
    def __init__(self, chromedriver_path="/usr/local/bin/chromedriver"):
        self.chromedriver_path = chromedriver_path

    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")
        chrome_options.add_argument("--start-maximized")
        chrome_options.page_load_strategy = 'eager'

        return webdriver.Chrome(self.chromedriver_path, options=chrome_options)

    def __get_google_top_result(self, driver):
        html_content = driver.page_source
        name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"{name}.txt", "w", encoding="utf-8") as f:
            f.write(html_content)
        data = BSHTMLLoader(f"{name}.txt"
                            ).load()
        data = "".join(data[0].page_content.split("\n")[1:6])
        os.remove(f"{name}.txt")
        return data, html_content

    def search(self, query, num_results=10, filename="search_result_html.txt") -> SearchResult:
        driver = self._setup_driver()
        try:
            driver.get("https://www.google.com")

            search_box = driver.find_element(By.NAME, "q")
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)

            WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((By.ID, "search"))
            )

            results = driver.find_elements(By.CSS_SELECTOR, "div.g")
            search_results = []
            for result in results[:num_results]:  # Limit to first 10 results for speed
                try:
                    title = result.find_element(By.CSS_SELECTOR, "h3").text
                    link = result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                    search_results.append({"title": title, "link": link})
                except:
                    continue
            google_response, html_content = self.__get_google_top_result(driver)
            urls = [x['link'] for x in search_results]

            return SearchResult(title_and_links=search_results,
                                google_top_response=google_response,
                                html_content=html_content,
                                urls=urls)
        except:
            return SearchResult(title_and_links=[],
                                google_top_response="",
                                html_content="",
                                urls=[])
        finally:
            driver.quit()


