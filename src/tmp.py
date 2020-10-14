# coding: utf-8

from pixivpy3 import *
import json
from time import sleep
import os
from tqdm import tqdm
import sys
import numpy as np
import queue
aapi = AppPixivAPI()
f = open('id_info.json', 'r')
client_info = json.load(f)
f.close()
aapi.login(client_info['pixiv_id'], client_info['password'])

json_result = aapi.search_user("musshu")
print(json_result)
json_result = aapi.search_user("gomzi")
print(json_result)
illust = json_result.user_previews[0].illusts[0]
print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))
