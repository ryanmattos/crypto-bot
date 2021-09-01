import os
import time
# from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
import requests
import pytz
from datetime import datetime
import logging as cryptoLogging
from crypto import Crypto, btc, eth, ada, dog, oldEth, oldBtc, oldAda, oldDog
from functions import checkChanges

WAIT_REQUEST = 600
CURRENCY_SLUG = 'U$'

def fetch_crypto():
   cryptoLogging.basicConfig(filename='logs/cryptos.log', filemode='w', format='%(asctime)s:: %(message)s', level=cryptoLogging.INFO)
   cryptoLogger = cryptoLogging.getLogger()

   params = {'symbol': 'btc,eth,ada,doge', 'convert': 'USD'}
   response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
   
   tz = pytz.timezone('Brazil/East')
   dt = datetime.now(tz)
   req = datetime.strftime(dt, "%H:%M")
   
   btcPrice = response['data']['BTC']['quote']['USD']['price']
   ethPrice = response['data']['ETH']['quote']['USD']['price'] 
   adaPrice = response['data']['ADA']['quote']['USD']['price'] 
   dogPrice = response['data']['DOGE']['quote']['USD']['price'] 
   
   btcRounded = round(btcPrice,2)
   ethRounded = round(ethPrice,2)
   adaRounded = round(adaPrice,2)
   dogRounded = round(dogPrice,2)
   

   # #set the old btc now
   oldBtc.price = btcPrice
   oldBtc.formatted = btcRounded
   
   oldEth.price = ethPrice
   oldEth.formatted = ethRounded
   
   oldAda.price = adaPrice
   oldAda.formatted = adaRounded
   
   oldDog.price = dogPrice
   oldDog.formatted = dogRounded
      
   # #set the cryptos that will be the latest ones
   btc.price = btcPrice
   btc.formatted = btcRounded
   btc.lastRequest = req
   
   eth.price = ethPrice
   eth.formatted = ethRounded
   eth.lastRequest = req
   
   ada.price = adaPrice
   ada.formatted = adaRounded
   ada.lastRequest = req
   
   dog.price = dogPrice
   dog.formatted = dogRounded
   dog.lastRequest = req
   
   cryptoLogger.info(f'FIRST LOG: BTC\t{CURRENCY_SLUG}{btcRounded}')
   cryptoLogger.info(f'FIRST LOG: ETH\t{CURRENCY_SLUG}{ethRounded}')
   cryptoLogger.info(f'FIRST LOG: ETH\t{CURRENCY_SLUG}{adaRounded}')
   cryptoLogger.info(f'FIRST LOG: ETH\t{CURRENCY_SLUG}{dogRounded}')
   
   print("running")
   time.sleep(WAIT_REQUEST)
   while True:
      try:         
         print("\n[ FETCHING INFO ]")
         response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
         
         btc.price = response['data']['BTC']['quote']['USD']['price']
         eth.price = response['data']['ETH']['quote']['USD']['price']
         ada.price = response['data']['ADA']['quote']['USD']['price']
         dog.price = response['data']['DOGE']['quote']['USD']['price']
                  
         btc.formatted = round(btc.price,2)
         eth.formatted = round(eth.price,2)
         ada.formatted = round(ada.price,2)
         dog.formatted = round(dog.price,2)
                  
         print(f'  BTC - from: R${oldBtc.formatted}\tto: {CURRENCY_SLUG}{btc.formatted}')
         print(f'  ETH - from: R${oldEth.formatted}\tto: {CURRENCY_SLUG}{eth.formatted}')
         print(f'  ADA - from: R${oldAda.formatted}\tto: {CURRENCY_SLUG}{ada.formatted}')
         print(f'  DOGE - from: R${oldDog.formatted}\tto: {CURRENCY_SLUG}{dog.formatted}')
         
         if btc.price == oldBtc.price and eth.price == oldEth.price and ada.price == oldAda.price and dog.price == oldDog.price:
            time.sleep(WAIT_REQUEST)
            
            continue

         else:
            # notify
            print('[ PRICES CHANGED ]')

            checkChanges(btc, oldBtc)
            checkChanges(eth, oldEth)  
            checkChanges(ada, oldAda)
            checkChanges(dog, oldDog)

            time.sleep(WAIT_REQUEST)
            
            continue
         
               
      # To handle exceptions
      except Exception as e:
         print(f"error {e}")

