import datetime, time
import random
from parse import *
import re
import platform

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
            response = "@{} 🤖 replyman (https://github.com/yuderobot/replyman {}) を実行中です。サーバー: {}".format(status.user.screen_name, get_hash(), platform.platform())
        
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