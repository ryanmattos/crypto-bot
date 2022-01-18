import os
import time
import requests
import pytz
from datetime import datetime
import logging as cryptoLogging
from crypto import Crypto, btc, eth, ada, dog
from functions import checkChanges, overview

WAIT_REQUEST = 600
CURRENCY_SLUG = 'U$'

def fetch_crypto():
   cryptos = [btc, eth, ada, dog]
   
   cryptoLogging.basicConfig(filename='logs/cryptos.log', filemode='w', format='%(asctime)s:: %(message)s', level=cryptoLogging.INFO)
   cryptoLogger = cryptoLogging.getLogger()

   params = {'symbol': 'btc,eth,ada,doge', 'convert': 'USD'}
   response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()

   tz = pytz.timezone('America/Los_Angeles')
   dt = datetime.now(tz)
   req = datetime.strftime(dt, "%H:%M")
   
   for crypto in cryptos:
      price = response['data'][crypto.slug]['quote']['USD']['price']
      rounded = round(price, 4 if crypto.slug == 'DOGE' else 2)
      crypto.old.price = price
      crypto.old.formatted = rounded
      
      crypto.first.price = price
      crypto.first.formatted = rounded
      
      crypto.price = price
      crypto.formatted = rounded
      crypto.lastRequest = req
      
      cryptoLogger.info(f'FIRST LOG: {crypto.slug}\t{CURRENCY_SLUG}{rounded}')
   
   print("running")
   time.sleep(WAIT_REQUEST)
   while True:
      try:         
         print("\n[ FETCHING INFO ]")
         response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
         newDt = datetime.now(tz)
         
         for crypto in cryptos:
            crypto.price = response['data'][crypto.slug]['quote']['USD']['price']
            crypto.formatted = round(crypto.price, 4 if crypto.slug == 'DOGE' else 2)
            print(f'  {crypto.slug} - from: {CURRENCY_SLUG}{crypto.old.formatted}\tto: {CURRENCY_SLUG}{crypto.formatted}')
         
         if btc.price == btc.old.price and eth.price == eth.old.price and ada.price == ada.old.price and dog.price == dog.old.price:
            if isAnotherDay(dt, newDt):
               overview(cryptos)
               
            time.sleep(WAIT_REQUEST)
            
            continue

         else:
            # notify
            print('[ PRICES CHANGED ]')

            for crypto in cryptos:
               checkChanges(crypto)
           
            if isAnotherDay(dt, newDt):
               print('[ ANOTHER DAY, PRINT OVERVIEW ]')
               overview(cryptos)
            else:
               print(f'[ SAME DAY {dt.day} != {newDt.day}, KEEP GOING ]')
               
            time.sleep(WAIT_REQUEST)
            
            continue
         
               
      # To handle exceptions
      except Exception as e:
         print(f"error {e}")

def isAnotherDay(date, newDate):
   print('\n[ CHECKING DAY ]\n')
   return date.day != newDate.day