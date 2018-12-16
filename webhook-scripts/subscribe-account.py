from TwitterAPI import TwitterAPI
import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

ENVNAME = 'prod' #os.environ.get('ENVNAME', None)

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:prod/subscriptions', None, None, 'POST')

#TODO: check possible status codes and convert to nice messages
print (r.status_code)
       
