
import yfinance as yf
from datetime import datetime
import pandas as pd
ticker='msft'


tick = yf.Ticker(ticker)
x = tick.news
import yfinance as yf
from datetime import datetime, timezone
import pandas as pd

ticker = 'agzd'
tick = yf.Ticker(ticker)
x = tick.news
print(x)

# # Create an empty list to store the news data
# data = []

# # Iterate over each item in x and append it to the list
# for news_item in x:
#     timestamp = news_item['providerPublishTime']
#     datetime_obj = datetime.fromtimestamp(timestamp, timezone.utc)
#     formatted_date = datetime_obj.strftime("%Y-%m-%d")
#     data.append({'title': news_item['title'], 'publisher': news_item['publisher'], 'time': formatted_date, 'link': news_item['link']})

# # Create DataFrame from the list of dictionaries
# df = pd.DataFrame(data)

for i in range(3):
    print(f"\nNews {i}\n")
    timestamp = x[i]['providerPublishTime']
    datetime_obj = datetime.fromtimestamp(timestamp, timezone.utc)
    formatted_date = datetime_obj.strftime("%Y-%m-%d")
    print(f"Title: {x[i]['title']}")
    print(f"Publisher: {x[i]['publisher']}")
    print(f"Time: {timestamp}")
    print(f"Link: {x[i]['link']}")
