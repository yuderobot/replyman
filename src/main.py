# -*- coding: utf-8 -*-
import tweepy
import os
from os.path import join, dirname
from dotenv import load_dotenv
import random
import numpy as np
from parse import *

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

# Dice rolling
def dice(dice_size):
    num = np.random.randint(1, int(dice_size))
    return num

def simple_dice(dice_size, dice_num):
    dice_val = np.array([], dtype=np.int64)
    for i in range(dice_num):
        dice_val = np.append(dice_val, dice(dice_size))
    msg = '🎲: ' + str(np.sum(dice_val)) + ' = ' + str(dice_val)
    return msg

def gen_msg(status):
    response = "@{} 処理中に何らかの問題が発生しました。".format(status.user.screen_name)
    
    # Rock-paper-scisors logic
    if "グー" in status.text or "チョキ" in status.text or "パー" in status.text:
        response = "@{} {}".format(status.user.screen_name, random.choice(("グー", "チョキ", "パー")))

    # Commands
    else:
        msg = parse('@yuderobot {} {}', status.text)
        if msg:
            # Dice rolling
            if "dice" in msg[0]:
                dice = parse('@yuderobot dice {}d{}', status.text)
                if dice:
                    if dice[1].isdecimal() and dice[0].isdecimal():
                        dice_num = int(dice[0])
                        dice_size = int(dice[1])
                        m = simple_dice(dice_size, dice_num)
                    response = "@{} {}".format(status.user.screen_name, m)
            
            # Echo
            elif "echo" in msg[0]:
                if status.user.screen_name == "@yude_jp" or "@yude_RT":
                    response = "@{} echo: {}".format(status.user.screen_name, msg[1])
                else:
                    response = "@{} echo: 許可されていないアカウントです。".format(status.user.screen_name)
            
            else:
                response = "@{} あなたのツイートは {} 点です＞＜".format(status.user.screen_name, random.randint(0, 100))
    
    if (len(response) > 130):
        response = response[:130] + "..."
    return response

# Twitter streaming
class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print("[Info] Retrieved tweet: ", status.text)
        reply_msg = gen_msg(status)
        if "@yuderobot" in reply_msg:
            pass
            print("[Info] This tweet contains reply to yuderobot, skipped.")
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
