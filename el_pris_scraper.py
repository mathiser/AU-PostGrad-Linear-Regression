import datetime
import requests
import json
import pandas as pd
import time
from multiprocessing.pool import ThreadPool
def scrape_prices(start_date: str = "2021-01-01", end_date: str = "2022-01-01", region="DK1"):
    sd = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    ed = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    prices = []
    tmp_date = sd
    dates = []
    while tmp_date <= ed:
        dates.append(tmp_date)
        tmp_date += datetime.timedelta(days=1)
    def scrape(d, reg):
        res = requests.get(f'https://nrgi.dk/api/common/pricehistory?region={reg}&date={d.strftime("%Y-%m-%d")}')
        print(d)
        if res.ok:
            return res.json()
    
    p = ThreadPool(32)
    responses = p.starmap(scrape, [(d, region) for d in dates])
    p.close()
    p.join()
    prices = pd.concat([pd.DataFrame(res) for res in responses])
    prices.to_csv("prices.csv")
    

scrape_prices()