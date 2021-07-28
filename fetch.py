import os
import time
# from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
import requests
import logging as cryptoLogging
from notify import tweet

def calculate_variance(oldV, newV):
   return (float(oldV) - float(newV)) / float(oldV) * -1

def fetch_crypto(crypto):
   cryptoLogging.basicConfig(filename='cryptos.log', filemode='w', format='%(asctime)s:: %(message)s', level=cryptoLogging.INFO)
   cryptoLogger = cryptoLogging.getLogger()

   params = {'symbol': 'btc,eth', 'convert': 'BRL'}
   response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
   
   btcPrice = response['data']['BTC']['quote']['BRL']['price']
   ethPrice = response['data']['ETH']['quote']['BRL']['price']
   # print(f'bitcoin: {btcPrice} | eth: {ethPrice}')
   

   btcRounded = round(btcPrice,2)
   ethRounded = round(ethPrice,2)

   cryptoLogger.info(f'FIRST LOG: BTC\tR${btcRounded}')
   cryptoLogger.info(f'FIRST LOG: ETH\tR${ethRounded}')
   
   print("running")
   time.sleep(10)
   while True:
      try:         
         print("\n[ FETCHING INFO ]")
         response = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',params=params, headers={'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY']}).json()
         
         t = time.localtime()
         req = time.strftime("%H:%M", t)
         
         newBtcPrice = response['data']['BTC']['quote']['BRL']['price']
         newEthPrice = response['data']['ETH']['quote']['BRL']['price']
         # print(f'bitcoin: {btcPrice} | eth: {ethPrice}')
         

         newBtcRounded = round(newBtcPrice,2)
         newEthRounded = round(newEthPrice,2)

         print(f'  BTC - from: R${btcRounded}\tto: R${newBtcRounded}')
         print(f'  ETH - from: R${ethRounded}\tto: R${newEthRounded}')
         
         # check if new hash is same as the previous hash
         if newBtcPrice == btcPrice or newEthPrice == ethPrice:
            time.sleep(300)
            
            continue

         # if something changed in the hashes
         else:
            # notify
            print('[ PRICES CHANGED ]')
            
            if not newBtcPrice == btcPrice:
               varianceBtc = round(calculate_variance(btcPrice, newBtcPrice), 4)
               varianceOutputBtc = "{:.4f}".format(varianceBtc)
               cryptoLogger.info(f'BTC\t{varianceOutputBtc}%\tR$ {newBtcRounded}')
               differenceBtc = round(newBtcPrice - btcPrice,2)
               
               if varianceBtc > 0.005 or varianceBtc < -0.005:
                  if newBtcPrice > btcPrice:
                     print('  BTC - tweetting price up...\t\t\t[ OK ]')
                     tweet(f'Bitcoin subiu \U0001F60A   R${newBtcRounded}\n\U0001F4C8 Variação +{varianceOutputBtc}%  +R${differenceBtc}\n\n{req}')
                  else:
                     print('  BTC - tweetting price down...\t\t\t[ OK ]')
                     differenceBtc *= -1
                     tweet(f'Bitcoin caiu \U0001F633   R${newBtcRounded}\n\U0001F4C9 Variação {varianceOutputBtc}%  -R${differenceBtc}\n\n{req}')
               
                  btcPrice = newBtcPrice
                  btcRounded = round(newBtcPrice,2)
                  
               else:
                  print(f'  BTC - Not enough variance.\t{varianceBtc}%\t\t[ FAIL ]')
               
            if not newEthPrice == ethPrice:
               varianceEth = round(calculate_variance(ethPrice, newEthPrice), 4)          
               varianceOutputEth = "{:.4f}".format(varianceEth)
               cryptoLogger.info(f'ETH\t{varianceOutputEth}%\tR$ {newEthRounded}')
               differenceEth = round(newEthPrice - ethPrice,2)
               
               if varianceEth > 0.007 or varianceEth < -0.007:
                  if newEthPrice > ethPrice:
                     print('  ETH - tweetting price up...\t\t\t[ OK ]')
                     tweet(f'Ethereum subiu \U0001F60A   R${newEthRounded}\n\U0001F4C8 Variação +{varianceOutputEth}%  +R${differenceEth}\n\n{req}')
                  else:
                     print('  ETH - tweetting price down...\t\t\t[ OK ]')
                     tweet(f'Ethereum caiu \U0001F633   R${newEthRounded}\n\U0001F4C9 Variação {varianceOutputEth}%  -R${differenceEth}\n\n{req}')
               
                  ethPrice = newEthPrice
                  ethRounded = round(newEthPrice,2)
               else:
                  print(f'  ETH - Not enough variance.\t{varianceEth}%\t\t[ FAIL ]')
            
            time.sleep(300)
            
            continue
         
               
      # To handle exceptions
      except Exception as e:
         print(f"error {e}")

