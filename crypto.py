class Crypto:
   def __init__(self, slug, name, price=0, formatted=0, variance=0, cap=0, lastRequest=0):
      self.slug = slug
      self.name = name
      self.price = price
      self.formatted = formatted
      self.variance = variance
      self.cap = cap
      self.lastRequest = lastRequest
      
      