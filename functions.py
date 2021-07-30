from notify import tweet
import pytz
from datetime import datetime

def calculate_variance(oldV, newV):
   return (float(oldV) - float(newV)) / float(oldV) * -1

def checkChanges(crypto, oldCrypto):
   tz = pytz.timezone('Brazil/East')
   dt = datetime.now(tz)
   req = datetime.strftime(dt, "%H:%M")
   
   crypto.lastRequest = req
   
   if not crypto.price == oldCrypto.price:
      variance = round(calculate_variance(oldCrypto.price, crypto.price), 4)
      crypto.variance = "{:.4f}".format(variance)
      diff = round(crypto.price - oldCrypto.price, 2)
      
      if variance > crypto.cap or variance < crypto.cap * -1:
         if crypto.price > oldCrypto.price:
            print(f'  {crypto.slug} - tweeting price up...\t\t\t[  OK  ]')
            tweet(f'\U0001F60A [{crypto.slug}] {crypto.name} has gone up\n\U0001F4B5 R${crypto.formatted}\n\U0001F4C8 Variance +{crypto.variance}%  +R${diff}\n\nUpdated at {req}h')
         else:
            print(f'  {crypto.slug} - tweeting price down...\t\t\t[  OK  ]')
            diff *= -1
            tweet(f'\U0001F633 [{crypto.slug}] {crypto.name} has gone down\n\U0001F4B5 R${crypto.formatted}\n\U0001F4C9 Variance {crypto.variance}%  -R${diff}\n\nUpdated at {req}h')
         
         oldCrypto.price = crypto.price
         oldCrypto.formatted = crypto.formatted
         oldCrypto.lastRequest = crypto.lastRequest
         
      else:
         print(f'  {crypto.slug} - Not enough variance\t{abs(variance)}%\t\t[ FAIL ]')