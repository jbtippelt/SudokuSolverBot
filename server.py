#!/usr/bin/env python
from flask import Flask, request, send_from_directory, make_response
from http import HTTPStatus
import main, hashlib, hmac, base64, os, logging, json

CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
CURRENT_USER_ID = int(os.environ.get('CURRENT_USER_ID'))
	     
app = Flask(__name__)	 

#The GET method for webhook should be used for the CRC check
#TODO: add header validation (compare_digest https://docs.python.org/3.6/library/hmac.html)
@app.route("/webhook", methods=["GET"])
def twitterCrcValidation():
    
    crc = request.args['crc_token']
  
    validation = hmac.new(
        key=bytes(CONSUMER_SECRET, 'utf-8'),
        msg=bytes(crc, 'utf-8'),
        digestmod = hashlib.sha256
    )
    digested = base64.b64encode(validation.digest())
    response = {
        'response_token': 'sha256=' + format(str(digested)[2:-1])
    }
    print('responding to CRC call')

    return json.dumps(response)   
        
#The POST method for webhook should be used for all other API events
#TODO: add event-specific behaviours beyond Direct Message and Like
@app.route("/webhook", methods=["POST"])
def twitterEventReceived():
	  		
    requestJson = request.get_json()

    #dump to console for debugging purposes
    #print(json.dumps(requestJson, indent=4, sort_keys=True))
            
    if 'tweet_create_events' in requestJson.keys():
        #Tweet Favourite Event, process that
        likeObject = requestJson['tweet_create_events'][0]
        userId = likeObject.get('user', {}).get('id')
        username = likeObject.get('user', {}).get('screen_name')
        twtId = likeObject.get('id_str')          

        
        #event is from myself so ignore (Favourite event fires when you send a DM too)   
        if userId == CURRENT_USER_ID:
            print("Received own tweet with tweet-id " + twtId)
            return ('', HTTPStatus.OK)

        if likeObject.get('in_reply_to_status_id'):
            print("Received a reply to tweet-id " + twtId)
            return ('', HTTPStatus.OK)

        print("Received tweet from" + username + " with tweet-id " + twtId)
        main.solveTweet(likeObject, True)           
        #Twitter.processLikeEvent(likeObject)
                
    else:
        #Event type not supported
        return ('', HTTPStatus.OK)
    
    return ('', HTTPStatus.OK)

                	    
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 9020.
    port = int(os.environ.get('PORT',9020))
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(host='0.0.0.0', port=port, debug=True)
