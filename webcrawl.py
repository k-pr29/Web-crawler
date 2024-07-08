import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

def crawl_website(url, depth, max_depth, visited):
    if depth > max_depth:
        return

    # Check if the URL is already visited
    if url in visited:
        return

    # Mark the URL as visited
    visited.add(url)
    
    # Add headers to mimic a real browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Send a GET request to the website
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage: {url}. Error: {e}")
        return
    
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the page title
    title = soup.find('title')
    if title:
        print(f"{'  ' * depth}Depth {depth} - Title: {title.get_text().strip()}")
    else:
        print(f"{'  ' * depth}Depth {depth} - No title found for URL: {url}")
    
    # Extract and print the data you are interested in, e.g., article titles, paragraphs, etc.
    # For demonstration, let's print the first paragraph if available
    paragraph = soup.find('p')
    if paragraph:
        print(f"{'  ' * depth}Depth {depth} - First paragraph: {paragraph.get_text().strip()[:100]}...")

    # Find all links on the current page
    links = soup.find_all('a', href=True)
    
    sub_links = []
    for link in links:
        href = link['href']
        full_url = urljoin(url, href)
        
        # Ensure we only crawl the same domain and avoid already visited links
        if urlparse(full_url).netloc == urlparse(url).netloc and full_url not in visited:
            sub_links.append(full_url)
    
    # Print sub-links found on the current page
    if sub_links:
        print(f"{'  ' * depth}Depth {depth} - Sub-links:")
        for sub_link in sub_links:
            print(f"{'  ' * (depth + 1)}Depth {depth + 1} - {sub_link}")
    
    # Crawl each sub-link
    for sub_link in sub_links:
        time.sleep(1)  # Pause briefly to avoid overloading the server
        crawl_website(sub_link, depth + 1, max_depth, visited)

if __name__ == "__main__":
    # URL of the website to crawl
    starting_url = "https://docs.nvidia.com/cuda/"  # Replace with the website you want to crawl
    max_depth = 5
    visited_urls = set()
    crawl_website(starting_url, 0, max_depth, visited_urls)
