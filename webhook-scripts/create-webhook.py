from TwitterAPI import TwitterAPI
import sys, os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

ENV_LABEL = os.environ.get('ENV_LABEL')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:%s/webhooks' % ENV_LABEL, {'url': WEBHOOK_URL})

print (r.status_code)
print (r.text)