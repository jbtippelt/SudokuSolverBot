from TwitterAPI import TwitterAPI
import sys, os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

#The environment name for the beta is filled below. Will need changing in future		
ENVNAME = 'prod' #os.environ.get('ENVNAME', None)
WEBHOOK_URL = sys.argv[1]

twitterAPI = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

r = twitterAPI.request('account_activity/all/:prod/webhooks', {'url': WEBHOOK_URL})

print (r.status_code)
print (r.text)


'''


curl --request POST --url 'https://api.twitter.com/1.1/account_activity/all/:ENV_NAME/webhooks.json?url=https%3A%2F%2Feddie.jboka.de%2Fsuso%2Fwebhook%2Ftwitter' --header 'authorization: OAuth oauth_consumer_key="lmNQ13LTSKWX8Jc5iybszJkG3", oauth_nonce="da39a3ee5e6b4b0d3255bfef95601890afd80709", oauth_signature="GENERATED", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1544222595", oauth_token="1070291557872558080-6voJmD0BP362jrVAXCl51KGUeLnald", oauth_version="1.0"'


'''