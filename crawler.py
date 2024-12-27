import asyncio
import aiohttp
import logging
from utils import find_product_urls, fetch_dynamic_page_with_selenium

# Function to fetch the content of a page (using aiohttp)
async def fetch_page(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                logging.error(f"Failed to fetch {url} with status code {response.status}")
                return None
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

# Main crawling function for a given domain
async def crawl_domain(session, domain, use_selenium=False):
    product_urls = set()
    logging.info(f"Crawling {domain}...")
    
    # Base URL for the domain
    base_url = f"http://{domain}"
    
    if use_selenium:
        # Fetch dynamic content using Selenium if required
        page_content = fetch_dynamic_page_with_selenium(base_url)
    else:
        # Fetch the page using aiohttp
        page_content = await fetch_page(session, base_url)
    
    if page_content:
        product_urls.update(find_product_urls(page_content, base_url))

    # Return the discovered product URLs
    return product_urls

# Main function to start crawling for all domains
async def main():
    # Read domains from the urls.txt file
    domains = []
    with open('urls.txt', 'r') as f:
        domains = [line.strip() for line in f.readlines()]

    # Create an asynchronous session for HTTP requests
    async with aiohttp.ClientSession() as session:
        all_product_urls = {}

        # Create a list of tasks for each domain, assuming we want to use Selenium for certain domains
        tasks = [crawl_domain(session, domain, use_selenium=domain in ['example1.com', 'example2.com']) for domain in domains]
        
        # Run all tasks concurrently
        results = await asyncio.gather(*tasks)

        # Map results to domain URLs
        for domain, urls in zip(domains, results):
            all_product_urls[domain] = list(urls)

        # Save the results in a structured format
        with open("discovered_product_urls.txt", "w") as f:
            for domain, urls in all_product_urls.items():
                f.write(f"{domain}:\n")
                for url in urls:
                    f.write(f"  {url}\n")
        
        logging.info("Crawling complete. Product URLs saved.")

# Start the crawling process
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
