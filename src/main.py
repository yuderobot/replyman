# -*- coding: utf-8 -*-
from requests import NullHandler
import tweepy
import os
import datetime, time
from os.path import join, dirname
from dotenv import load_dotenv
import random
from parse import *
import re
from dice import simple_dice
from uptime import get_uptime
from git_hash import get_hash
from wol import issue_wol
import platform

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

# Initial datetime for uptime command
global start_time
start_time = datetime.datetime.utcnow()

def gen_msg(status):
    response = "@{} 処理中に何らかの問題が発生しました。".format(status.user.screen_name)

    # Commands
    msg = parse('@yuderobot {}', status.text)
    if msg:
        # Dice rolling
        if "dice" in msg[0]:
            dice = parse('@yuderobot dice {}d{}', status.text)
            if dice:
                response = "@{} {}".format(status.user.screen_name, simple_dice(dice[1], dice[0]))
            else:
                response = "@{} 🎲 dice: 「dice 2d100」のようにリプライしてください。".format(status.user.screen_name)
        
        # Wake on LAN
        if "wol" in msg[0]:
            if status.user.screen_name == "@yude_jp" or status.user.screen_name == "@yude_RT":
                msg = parse('@yuderobot wol {}', status.text)
                if msg:
                    result = issue_wol(msg[0])
                    if result == True:
                        response = "@{} 🌝 WoL: {} にマジックパケットを送信しました。".format(status.user.screen_name, msg[0])
                    else:
                        response = "@{} 🌝 WoL: {} というホストは登録されていません。".format(status.user.screen_name, msg[0])
            else:
                response = "@{} 🌝 WoL: コマンドの実行が許可されていないアカウントです。".format(status.user.screen_name)
        
        # echo
        elif "echo" in msg[0]:
            echo = parse('@yuderobot echo {}', status.text)
            if status.user.screen_name == "@yude_jp" or "@yude_RT":
                response = "@{} 📢 echo: {}".format(status.user.screen_name, echo[0])
            else:
                response = "@{} 📢 echo: コマンドの実行が許可されていないアカウントです。".format(status.user.screen_name)
        
        # version
        elif "ver" in msg[0]:
            response = "@{} 🤖 replyman (https://github.com/yuderobot/replyman {}), サーバー: {}".format(status.user.screen_name, get_hash(), platform.platform())
        
        # uptime
        elif "uptime" in msg[0]:
            delta = datetime.datetime.utcnow() - start_time
            response = "@{} ⌚ uptime: {}".format(status.user.screen_name, get_uptime(delta))
        
        # Greetings
        elif re.compile("(?:こん(?:にち|ばん)(?:は|わ)|や(?:ぁ|あ))").search(msg[0]):
            response = "@{} こんにちは!".format(status.user.screen_name)
        elif re.compile("hi|hello", re.IGNORECASE).search(msg[0]):
            greetings = random.choice(("Hello, what's up?", "Hi! How is it going?", "Hello, how are you doing?"))
            response = "@{} {}".format(status.user.screen_name, greetings)
        
        # Rock-paper-scisors
        elif re.compile("(?:[ぐぱグパ]ー|ちょき|チョキ)").search(msg[0]):
            result = random.choice(("グー", "チョキ", "パー"))
            response = "@{} {}".format(status.user.screen_name, result)
        
        # Scoring tweet
        else:
            response = "@{} あなたのツイートは {} 点です＞＜".format(status.user.screen_name, random.randint(0, 100))
    
    if (len(response) > 130):
        response = response[:120] + " ...(省略)"
    return response

# Twitter streaming
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


if __name__ == "__main__":
    listener = StreamListener()

stream = TweetStream(auth, listener)

stream.start()
