import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# List of product URL patterns to match
PRODUCT_URL_PATTERNS = [
    r"/product/", r"/item/", r"/p/"
]

# Function to discover product URLs from page content
def find_product_urls(page_content, base_url):
    soup = BeautifulSoup(page_content, 'html.parser')
    product_urls = set()

    # Look for links in the page and match product URL patterns
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        
        # Match common product URL patterns
        if any(re.search(pattern, href) for pattern in PRODUCT_URL_PATTERNS):
            full_url = href if href.startswith("http") else base_url + href
            product_urls.add(full_url)
    
    return product_urls

# Function to fetch a dynamic page with Selenium
def fetch_dynamic_page_with_selenium(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    
    return page_content
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# List of product URL patterns to match
PRODUCT_URL_PATTERNS = [
    r"/product/", r"/item/", r"/p/"
]

# Function to discover product URLs from page content
def find_product_urls(page_content, base_url):
    soup = BeautifulSoup(page_content, 'html.parser')
    product_urls = set()

    # Look for links in the page and match product URL patterns
    for anchor in soup.find_all('a', href=True):
        href = anchor['href']
        
        # Match common product URL patterns
        if any(re.search(pattern, href) for pattern in PRODUCT_URL_PATTERNS):
            full_url = href if href.startswith("http") else base_url + href
            product_urls.add(full_url)
    
    return product_urls

# Function to fetch a dynamic page with Selenium
def fetch_dynamic_page_with_selenium(url):
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    
    driver.get(url)
    page_content = driver.page_source
    driver.quit()
    
    return page_content
