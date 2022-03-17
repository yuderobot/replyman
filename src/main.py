# -*- coding: utf-8 -*-

# functions
from dice import simple_dice
from uptime import get_uptime
from git_hash import get_hash
from wol import issue_wol
from stream import get_stream

if __name__ == "__main__":
    get_stream().start()