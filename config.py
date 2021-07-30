import os
import tweepy
import logging

logging.basicConfig(filename='logs/.log', filemode='w', format='%(asctime)s:: %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger()

def create_api():
   auth = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET'])
   auth.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])

   # Create API object
   api = tweepy.API(auth, wait_on_rate_limit=True,
      wait_on_rate_limit_notify=True)

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