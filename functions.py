from notify import tweet
import pytz
from datetime import datetime

def calculate_variance(oldV, newV):
   return (float(oldV) - float(newV)) / float(oldV) * -1

def checkChanges(crypto):
   # tz = pytz.timezone('Brazil/East')
   tz = pytz.timezone('America/Los_Angeles')
   dt = datetime.now(tz)
   req = datetime.strftime(dt, "%H:%M")
   
   crypto.lastRequest = req
   
   if not crypto.price == crypto.old.price:
      variance = round(calculate_variance(crypto.old.price, crypto.price), 4)
      crypto.variance = "{:.4f}".format(variance)
      if crypto.slug == "DOGE":
         diff = round(crypto.price - crypto.old.price, 3)
      else:
         diff = round(crypto.price - crypto.old.price, 2)
         
      if variance > crypto.cap or variance < crypto.cap * -1:
         if crypto.price > crypto.old.price:
            print(f'  {crypto.slug} - tweeting price up...\t\t\t[  OK  ]')
            tweet(f'\U0001F60A [ ${crypto.slug} ] {crypto.name} has gone up\n\U0001F4B5 ${crypto.formatted}\n\U0001F4C8 Variance +{crypto.variance}%  +${diff}\n\nUpdated at {req}h')
         else:
            print(f'  {crypto.slug} - tweeting price down...\t\t\t[  OK  ]')
            diff *= -1
            tweet(f'\U0001F633 [ ${crypto.slug} ] {crypto.name} has gone down\n\U0001F4B5 ${crypto.formatted}\n\U0001F4C9 Variance {crypto.variance}%  -${diff}\n\nUpdated at {req}h')
         
         crypto.old.price = crypto.price
         crypto.old.formatted = crypto.formatted
         crypto.old.lastRequest = crypto.lastRequest
         
      else:
         print(f'  {crypto.slug} - Not enough variance\t{abs(variance)}%\t\t[ FAIL ]')
         
def overview(cryptos):
   content = f'[ OVERVIEW 24HRS ]\n'
   content += f'This is the rank of cryptos by percentual variance.\n\n'
   
   cryptos.sort(key = lambda x: round(calculate_variance(x.first.price, x.price), 4))
   
   for idx, x in enumerate(cryptos):
      variance = round(calculate_variance(x.first.price, x.price), 4)
      variance = "{:.4f}".format(variance)
      if x.slug == "DOGE":
         diff = round(x.price - x.first.price, 3)
      else:
         diff = round(x.price - x.first.price, 2)
         
      if x.price > x.first.price:
         content += f'#{idx+1}\t\U0001F4C8 [ ${x.slug} ] {x.name}\t+{variance}% (${diff})\n'
      else:
         content += f'#{idx+1}\t\U0001F4C9 [ ${x.slug} ] {x.name}\t-{variance*-1}% (${diff*-1})\n'
         
      x.first.price = x.price
      x.first.format = x.formatted
      x.first.lastRequest = x.lastRequest
      
   print(f'{cryptos[0].slug} has raised the most\tU${cryptos[0].price}\t\t[ COOL ]')
   tweet(content)
   
   content = f'[ OVERVIEW 24HRS ]\n'
   content += f'This is the rank of cryptos by price variance.\n\n'
   
   cryptos.sort(key = lambda x: abs(round(x.first.price - x.price, 4)))
   
   for idx, x in enumerate(cryptos):
      variance = round(calculate_variance(x.first.price, x.price), 4)
      variance = "{:.4f}".format(variance)
      if x.slug == "DOGE":
         diff = round(x.price - x.first.price, 3)
      else:
         diff = round(x.price - x.first.price, 2)
         
      if x.price > x.first.price:
         content += f'#{idx+1}\t\U0001F4C8 [ ${x.slug} ] {x.name}\t+{variance}% (${diff})\n'
      else:
         content += f'#{idx+1}\t\U0001F4C9 [ ${x.slug} ] {x.name}\t-{variance*-1}% (${diff*-1})\n'
         
      x.first.price = x.price
      x.first.format = x.formatted
      x.first.lastRequest = x.lastRequest
      
   print(f'{cryptos[0].slug} has raised the most\tU${cryptos[0].price}\t\t[ COOL ]')
   tweet(content)
      