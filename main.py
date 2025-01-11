import json
from datetime import datetime as dt
from dotenv import load_dotenv
from crawler import Crawler

load_dotenv()

crawler = Crawler()

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error loading config data: {e}")
    exit(1)

prices_to_notify = []

for index, item in enumerate(config['items']):
    try:
        item_data = crawler.crawl(item['url'])
        
        if (item_data is None):
            continue

        if (item_data['price'] < item['target_price']):
            print(f"Price is below target price: {item_data['price']}")
            print(f"URL: {item['url']}")
            prices_to_notify.append(item)

        if (item_data['price'] < item['cheapest_price_found']):
            item['cheapest_price_found'] = item_data['price']

        # update the json data
        config['items'][index]['title'] = item_data['title']
        config['items'][index]['last_checked'] = dt.now().isoformat()
    except Exception as e:
        print(f"Error crawling page: {e}")
        print(f"URL: {item['url']}")
        exit(1)

try:
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
except Exception as e:
    print(f"Error writing to config file: {e}")

if (len(prices_to_notify) > 0):
    print(f"{len(prices_to_notify)} items were found that were below your target price\n")
    try:
        for item in prices_to_notify:
            print(f"Item: {item['title']}")
            print(f"Price: {item['price']}")
            print(f"URL: {item['url']}\n")
    except Exception as e:
        print(f"Error sending notification: {e}")
else:
    print("No items were found that were below your target price")
