import os
import time
# from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
import requests
import logging as cryptoLogging
from crypto import Crypto
from functions import checkChanges

WAIT_REQUEST = 10

def fetch_crypto():
   cryptoLogging.basicConfig(filename='logs/cryptos.log', filemode='w', format='%(asctime)s:: %(message)s', level=cryptoLogging.INFO)
   cryptoLogger = cryptoLogging.getLogger()

   params = {'symbol': 'btc,eth', 'convert': 'BRL'}
   response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
   
   btcPrice = response['data']['BTC']['quote']['BRL']['price']
   ethPrice = response['data']['ETH']['quote']['BRL']['price']   
   
   btcRounded = round(btcPrice,2)
   ethRounded = round(ethPrice,2)

   #set the old btc now
   oldBtc = Crypto(slug='BTC', name='Bitcoin', price=btcPrice, formatted=btcRounded, cap=0.005)
   oldEth = Crypto(slug='ETH', name='Ethereum', price=ethPrice, formatted=ethRounded, cap=0.007)
   
   #set the cryptos that will be the latest ones
   btc = Crypto(slug='BTC', name='Bitcoin', price=btcPrice, formatted=btcRounded, cap=0.005)
   eth = Crypto(slug='ETH', name='Ethereum', price=ethPrice, formatted=ethRounded, cap=0.007)
   
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

