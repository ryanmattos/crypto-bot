class Crypto:
   def __init__(self, slug, name, price=0, formatted=0, variance=0, cap=0, first=None, old=None, lastRequest=0):
      self.slug = slug
      self.name = name
      self.price = price
      self.formatted = formatted
      self.variance = variance
      self.cap = cap
      self.first = first
      self.old = old
      self.lastRequest = lastRequest

#set the cryptos that will be the latest ones
btc = Crypto(slug='BTC', name='Bitcoin', cap=0.005)
eth = Crypto(slug='ETH', name='Ethereum', cap=0.007)
ada = Crypto(slug='ADA', name='Cardano', cap=0.008)
dog = Crypto(slug='DOGE', name='Dogecoin', cap=0.008)
   
btc.old = Crypto(slug='BTC', name='Bitcoin', cap=0.005)
eth.old = Crypto(slug='ETH', name='Ethereum', cap=0.007)
ada.old = Crypto(slug='ADA', name='Cardano', cap=0.008)
dog.old = Crypto(slug='DOGE', name='Dogecoin', cap=0.008)

btc.first = Crypto(slug='BTC', name='Bitcoin', cap=0.005)
eth.first = Crypto(slug='ETH', name='Ethereum', cap=0.007)
ada.first = Crypto(slug='ADA', name='Cardano', cap=0.008)
dog.first = Crypto(slug='DOGE', name='Dogecoin', cap=0.008)
