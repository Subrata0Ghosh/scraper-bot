import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def scrape_data(url, max_pages=5, delay=2):
    results = []
    current_url = url
    page_count = 0

    try:
        while current_url and page_count < max_pages:
            print(f"Scraping page {page_count + 1}: {current_url}")
            response = requests.get(current_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all product entries
            products = soup.find_all('article', class_='product_pod')

            for product in products:
                title = product.h3.a['title']
                price = product.find('p', class_='price_color').text
                availability = product.find('p', class_='instock availability').text.strip()
                product_link = product.h3.a['href']
                full_link = urljoin(current_url, product_link)
                
                # Get product image URL (assuming it's stored in 'img' tag)
                img_tag = product.find('img')
                img_url = img_tag['src'] if img_tag else None
                full_img_url = urljoin(current_url, img_url) if img_url else None

                results.append({
                    "title": title,
                    "price": price,
                    "availability": availability,
                    "product_url": full_link,
                    "image_url": full_img_url  # Add image URL to the result
                })

            # Find the "next" button for pagination
            next_button = soup.select_one('li.next > a')
            if next_button:
                next_page_url = next_button['href']
                current_url = urljoin(current_url, next_page_url)
            else:
                current_url = None  # No more pages

            page_count += 1
            time.sleep(delay)

        return results

    except Exception as e:
        print(f"Error: {e}")
        return []


