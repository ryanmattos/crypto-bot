import threading
from fetch import fetch_crypto

exitFlag = 0

class fetchThread(threading.Thread):
   def __init__(self, crypto):
      threading.Thread.__init__(self)
      self.crypto = crypto

   def run(self):
      print("Starting " + self.crypto) 
      fetch_crypto(self.crypto)
      print("Exiting " + self.crypto)

thread1 = fetchThread('bitcoin')
# thread2 = fetchThread('ethereum')

thread1.start()
# thread2.start()