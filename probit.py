import os
import requests
import pandas as pd
import threading
import time
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import random

buy = 'buy'
sell = 'sell'
#ahten =
class probit(object):
#    def init(self):
    def fetchCurrency(self):
        url = "https://api.probit.com/api/exchange/v1/currency"
        response = requests.request("GET", url)
        print(response.text)

    def fetchTicker(self,id):
        url = "https://api.probit.com/api/exchange/v1/ticker"
        querystring = {"market_ids":id}
        response = requests.request("GET", url, params=querystring)
        print(response.text)

    def orderBook(self,id):
        url = "https://api.probit.com/api/exchange/v1/order_book"
        querystring = {"market_id":id}
        response = requests.request("GET", url, params=querystring)
        json_data = json.loads(response.text)
        pd.read_json(json.dumps(json_data['data'])).to_csv('unsorted.csv')
        df = pd.read_csv('unsorted.csv', index_col= 0)
        df1 = df.sort_values(['side', 'price'], ascending=[True, True])
        df1 = df1.reset_index(drop=True)
        df1.to_csv('data.csv')
        count = 0
        for i in df1['side']:
            if i == 'sell':
                break
            count+=1
        bookSell = float(df1.iloc[count]['price'])
        bookBuy = float(df1.iloc[count-1]['price'])
        res = []
        res.append(bookSell)
        res.append(bookBuy)
        return res

    def sign(self,authen):
        url = "https://accounts.probit.com/token"
        payload = "{\"grant_type\":\"client_credentials\"}"
        headers = {
            'authorization': authen,
            'content-type': "application/json"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        a = response.text
        token = a.split(":")
        return token[1][1:45]

    def getHeader(self):
        token = self.sign(authen)
        bearer = 'Bearer {}'.format(token)
        headers = {
            'content-type': "application/json",
            "authorization":bearer}
        return headers

    def getBalance(self):
        url = "https://api.probit.com/api/exchange/v1/balance"
        response = requests.request("GET", url, headers=self.getHeader())
        print(response.text)


    def getOrder(self,method,price,quantity,id):
        price = str(price)
        quantity = str(quantity)

        url = "https://api.probit.com/api/exchange/v1/new_order"
        payload = "{\"market_id\":\"id\",\"type\":\"limit\",\"side\":\"methodInput\",\"time_in_force\":\"gtc\",\"limit_price\":\"priceInput\",\"quantity\":\"quantityInput\"}"
        payload = payload.replace("id", str(id))
        payload = payload.replace("priceInput", str(price))
        payload = payload.replace("quantityInput",str(quantity))
        payload = payload.replace("methodInput", method)
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer [object Object]"
            }
        response = requests.request("POST", url, data=payload, headers=self.getHeader())
        print(response.text)

def sortOrder(unsorted):
    pd.read_json(json.dumps(unsorted['data'])).to_csv('unsorted.csv')
    df = pd.read_csv('unsorted.csv')
    df1 = df.sort_values(['side', 'price'], ascending=[True, True])
    df1.to_csv('data.csv')
