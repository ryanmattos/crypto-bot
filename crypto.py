class Crypto:
   def __init__(self, slug, name, price=0, formatted=0, variance=0, cap=0, lastRequest=0):
      self.slug = slug
      self.name = name
      self.price = price
      self.formatted = formatted
      self.variance = variance
      self.cap = cap
      self.lastRequest = lastRequest
   
oldBtc = Crypto(slug='BTC', name='Bitcoin', cap=0.005)
oldEth = Crypto(slug='ETH', name='Ethereum', cap=0.007)

#set the cryptos that will be the latest ones
btc = Crypto(slug='BTC', name='Bitcoin', cap=0.005)
eth = Crypto(slug='ETH', name='Ethereum', cap=0.007)
      