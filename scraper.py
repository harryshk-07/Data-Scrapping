import requests
from bs4 import BeautifulSoup

def scrape_website():
    url = "https://www.reddit.com"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        data = []
        # Adjust the class or tag selectors based on Reddit's structure
        for item in soup.find_all('div', class_='h-[210px] relative rounded-[16px] flex flex-col justify-end overflow-hidden carousel-item-cover'):
            title = item.find('h2')  # Finding the title inside the container
            description = item.find('p')  # Finding the description
            subreddit = item.find('span', class_='font-bold')  # Finding subreddit name
            image = item.find('img')  # Finding image URL

            if title and description and subreddit and image:
                data.append({
                    'title': title.text.strip(),
                    'description': description.text.strip(),
                    'subreddit': subreddit.text.strip(),
                    'image_url': image['src']
                })
        return data
    else:
        print(f"Failed to scrape {url}, status code: {response.status_code}")
        return []
