import os
import tweepy
import logging
from crypto import btc, eth, dog, ada

logging.basicConfig(filename='logs/.log', filemode='w', format='%(asctime)s:: %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

class TweetStreamListener(tweepy.StreamListener):
   def on_status(self, status):
      reply(status)
      
   def on_error(self, status_code):
      if status_code == 420:
         #returning False in on_error disconnects the stream
         return False

def create_api():
   auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET'])
   auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
   
   tweetListener = TweetStreamListener()

   # Create API object
   api = tweepy.API(auth, wait_on_rate_limit=True,
      wait_on_rate_limit_notify=True)
   tweetStream = tweepy.Stream(auth, listener=tweetListener)
   
   tweetStream.filter(track=['@cryptobipolar_'], is_async=True)

   try:
      api.verify_credentials()
   except Exception as e:
      logger.error("Error creating API", exc_info=True)
      raise e
   logger.info("API created")

   # Create a tweet
   # api.update_status("Test")

   return api

create_api()

def reply(status):
   api = create_api()
   
   tweet = status.text.replace("@cryptobipolar_ ", "")
   user = status.user.screen_name
   statusId = status.id
      
   if "btc" in tweet.lower():
      print(f'[ REPLY ]\nReplying user @{user} about BTC')
      api.update_status(f'\U0001F60A [{btc.slug}] {btc.name} price\n\U0001F4B5 ${btc.formatted}\n\nLast update at {btc.lastRequest}h', in_reply_to_status_id=statusId, auto_populate_reply_metadata=True)
   elif "eth" in tweet.lower():
      print(f'[ REPLY ]\nReplying user @{user} about ETH')
      api.update_status(f'\U0001F60A [{eth.slug}] {eth.name} price\n\U0001F4B5 ${eth.formatted}\n\nLast update at {eth.lastRequest}h', in_reply_to_status_id=statusId, auto_populate_reply_metadata=True)
   elif "doge" in tweet.lower():
      print(f'[ REPLY ]\nReplying user @{user} about DOGE')
      api.update_status(f'\U0001F60A [{dog.slug}] {dog.name} price\n\U0001F4B5 ${dog.formatted}\n\nLast update at {dog.lastRequest}h', in_reply_to_status_id=statusId, auto_populate_reply_metadata=True)
   elif "ada" in tweet.lower():
      print(f'[ REPLY ]\nReplying user @{user} about ADA')
      api.update_status(f'\U0001F60A [{ada.slug}] {ada.name} price\n\U0001F4B5 ${ada.formatted}\n\nLast update at {ada.lastRequest}h', in_reply_to_status_id=statusId, auto_populate_reply_metadata=True)