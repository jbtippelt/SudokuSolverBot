import image_processor as imp
import twitter, cv2, sys, os
from skimage import io


def auth():
    CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
    CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
    ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

    return twitter.Api (consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

def replyTweet(api, twt_id, twt_username, state):

    if state == 0:
        file_path = "solution.png"
        message = "@" + twt_username + " I solved your Sudoku! Is this the right solution?"
        api.PostUpdate(message, media=file_path, in_reply_to_status_id=twt_id)
    elif state == 1:
        message = "@" + twt_username + " I can not solve the sudoku. Sorry!"
        api.PostUpdate(message, in_reply_to_status_id=twt_id)
    elif state == 2:
        message = "@" + twt_username + " There is no sudoku to solve. Pleas add an image with a sudoku."
        api.PostUpdate(message, in_reply_to_status_id=twt_id)
    else:
        print("Nothing replyed!")
        return
    print ("-> Replyed !")

def solveTweet(twt, reply):
    api = auth()
    twt_username = twt["user"]["screen_name"]
    twt_id = twt["id"]
    if "media" in twt["entities"]:
        for media in twt["entities"]["media"]:
            if media["type"] == "photo":
                url = media["media_url"]
                print ("Try to solve tweet with id", twt_id)
                print(url)
                img = io.imread(url)
                solvedImg = imp.getSolvedImage(img)
                if solvedImg is not False:
                    file_path = "solution.png"
                    cv2.imwrite(file_path, solvedImg)
                    print ("-> Sudoku solved !")
                    message = "@" + twt_username + " I solved your Sudoku! Is this the right solution?"
                    if reply: replyTweet(api, twt_id, twt_username, 0)
                else:
                    print ("-> Couldn't solve Sudoku")
                    if reply: replyTweet(api, twt_id, twt_username, 1)
    else:
        print ("No image found in this tweet", twt_id)
        if reply: replyTweet(api, twt_id, twt_username, 2)

def solveWithHashtag(api, hashtag, reply):
    search = api.GetSearch(term=hashtag, count=20, result_type="recent", include_entities=True, return_json=True)

    for twt in search["statuses"]:
        solveTweet(api, twt, reply)

def main():

    api = auth()

    me_obj = api.GetUser(screen_name="easysudoku")
    me_json = me_obj._json
    me_id = me_json['id']
    print ("Hi I am", me_json["screen_name"], "and I solve your sudoku!", "\nMy id is", me_id)


if __name__ == '__main__': main()