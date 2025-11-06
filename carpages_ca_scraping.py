import requests
from bs4 import BeautifulSoup
import pandas as pd

def fun():
    base_url = 'https://www.carpages.ca'
    url = f'{base_url}/used-cars/search/?num_results=50&fueltype_id%5b0%5d=3&fueltype_id%5b1%5d=7&p=1'

    df_rows = []
    counter = 0

    while counter < 10:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')

        postings = soup.find_all('div', class_='tw:flex tw:gap-6 tw:items-start tw:p-6')

        for post in postings:
            try:
                link_tag = post.find('a', class_='tw:flex tw:items-start tw:w-[130px] tw:shrink-0')
                name_tag = post.find('h4', class_='hN')
                price_tag = post.find('span', class_='tw:font-bold tw:text-xl')
                color_tags = post.find_all('span', class_='tw:text-sm tw:font-bold')

                link = base_url + link_tag.get('href') if link_tag else None
                name = name_tag.text.strip() if name_tag else None
                price = price_tag.text.strip() if price_tag else None
                color = color_tags[1].text.strip() if len(color_tags) > 1 else None

                df_rows.append({'Link': link, 'Name': name, 'Price': price, 'Color': color})
            except Exception as e:
                print(f"Error parsing post: {e}")

        # Find next page
        next_page_tag = soup.find('a', class_='nextprev')
        if not next_page_tag or not next_page_tag.get('href'):
            print("No more pages found.")
            break

        url = next_page_tag.get('href')
        if not url.startswith('http'):
            url = base_url + url

        counter += 1
        print(f"Scraped page {counter}")

    df = pd.DataFrame(df_rows)
    df.to_csv('carpages_data.csv', index=False)
    print("Scraping complete. Data saved to carpages_data.csv")

if __name__ == "__main__":
    fun()

