import tweepy
import os
from os.path import join, dirname
from dotenv import load_dotenv
from message import gen_msg

# Import keys from .env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
CK = os.environ.get("CK")
CS = os.environ.get("CS")
AT = os.environ.get("AT")
AS = os.environ.get("AS")

# OAuth authentication
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

# Generate API instance
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print("[Info] Retrieved tweet: ", status.text)
        reply_msg = gen_msg(status)
        if "@yuderobot" in reply_msg:
            pass
            print("[Info] This tweet contains reply to yuderobot, skipped.")
        elif "RT" in status.text:
            pass
            print("[Info] This tweet is retweet, skipped.")
        else:
            api.update_status(reply_msg, in_reply_to_status_id=status.id)
            print("[Info] Sent tweet: {}".format(reply_msg))
        return True

    def on_error(self, status_code):
        if status_code == 420:
            print('[Error] 420')
            return False
        else:
            print(f'[Error] Unknown error occured: {status_code}')
            return False


class TweetStream():
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self):
        self.stream.filter(track=["@yuderobot"])

def get_stream():
    listener = StreamListener()
    return TweetStream(auth, listener)