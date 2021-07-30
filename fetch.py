import os
import time
# from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
import requests
import pytz
from datetime import datetime
import logging as cryptoLogging
from crypto import Crypto, btc, eth, oldEth, oldBtc
from functions import checkChanges

WAIT_REQUEST = 600

def fetch_crypto():
   cryptoLogging.basicConfig(filename='logs/cryptos.log', filemode='w', format='%(asctime)s:: %(message)s', level=cryptoLogging.INFO)
   cryptoLogger = cryptoLogging.getLogger()

   params = {'symbol': 'btc,eth', 'convert': 'BRL'}
   response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
   
   tz = pytz.timezone('Brazil/East')
   dt = datetime.now(tz)
   req = datetime.strftime(dt, "%H:%M")
   
   btcPrice = response['data']['BTC']['quote']['BRL']['price']
   ethPrice = response['data']['ETH']['quote']['BRL']['price']   
   
   btcRounded = round(btcPrice,2)
   ethRounded = round(ethPrice,2)

   # #set the old btc now
   oldBtc.price = btcPrice
   oldBtc.formatted = btcRounded
   
   oldEth.price = ethPrice
   oldEth.formatted = ethRounded
      
   # #set the cryptos that will be the latest ones
   btc.price = btcPrice
   btc.formatted = btcRounded
   btc.lastRequest = req
   
   eth.price = ethPrice
   eth.formatted = ethRounded
   eth.lastRequest = req
   
   cryptoLogger.info(f'FIRST LOG: BTC\tR${btcRounded}')
   cryptoLogger.info(f'FIRST LOG: ETH\tR${ethRounded}')
   
   print("running")
   time.sleep(WAIT_REQUEST)
   while True:
      try:         
         print("\n[ FETCHING INFO ]")
         response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
         
         btc.price = response['data']['BTC']['quote']['BRL']['price']
         eth.price = response['data']['ETH']['quote']['BRL']['price']
                  
         btc.formatted = round(btc.price,2)
         eth.formatted = round(eth.price,2)
         
         print(f'  BTC - from: R${oldBtc.formatted}\tto: R${btc.formatted}')
         print(f'  ETH - from: R${oldEth.formatted}\tto: R${eth.formatted}')
         
         if btc.price == oldBtc.price and eth.price == oldEth.price:
            time.sleep(WAIT_REQUEST)
            
            continue

         else:
            # notify
            print('[ PRICES CHANGED ]')

            checkChanges(btc, oldBtc)
            checkChanges(eth, oldEth)   

            time.sleep(WAIT_REQUEST)
            
            continue
         
               
      # To handle exceptions
      except Exception as e:
         print(f"error {e}")

