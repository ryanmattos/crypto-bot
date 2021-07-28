from config import create_api

def tweet(content):
   api = create_api()
   api.update_status(content)