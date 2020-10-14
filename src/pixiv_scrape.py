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
SAVE_DIR='../dataset/pixiv_images/'
os.makedirs(SAVE_DIR, mode=0o777, exist_ok=True)
uid=1774953

user_que=queue.Queue()
user_que.put(uid)

# duplicate_user=set()
# duplicate_user.add(uid)
with open('../log/pixiv_scrape_log.txt') as f:
    lines = f.read().splitlines()
    lines=[int(i) for i in lines]
duplicate_user=set(lines)

month=3
year=2020
while len(os.listdir(SAVE_DIR))<100000:
    # while user_que.empty():
    #     date=str(year)+'-'+str(month).rjust(2,'0')+'-01'
    #     print('extract from '+date+' ranking')
    #     res = aapi.illust_ranking('month', date=date)
    #     month-=1
    #     if month<1:
    #        month=12
    #        year-=1
    #        if year<2010:
    #            break
    #     print(len(res.illusts))
    #     for illust in res.illusts:
    #         if illust.user.id not in duplicate_user:
    #             user_que.put(illust.user.id)
    #             duplicate_user.add(illust.user.id)
    if user_que.empty():
        print('que_empty')
        break
    uid=user_que.get()
    f=open('../log/pixiv_scrape_log.txt','a')
    print(uid,file=f)
    try:
        json_result = aapi.user_illusts(uid)
        # print(len(json_result['illusts']))
        for illust in json_result['illusts']:
            # print("%d bookmarks" % illust['total_bookmarks'])
            if illust['total_bookmarks']>1000:
                # for tag in illust.tags:
                #     if tag.name=='\u5973\u306e\u5b50':    tag: onnanoko
                print(">>> origin url: %s" % illust.image_urls['large'])
                aapi.download(illust.image_urls['large'],SAVE_DIR)
                    
                sleep(1)
        try:
            for following in aapi.user_following(uid).user_previews:
                if following.user.id not in duplicate_user:
                    user_que.put(following.user.id)
                    duplicate_user.add(following.user.id)
        except KeyboardInterrupt:
            break
        except:
            print('no following')
            continue 
    except KeyboardInterrupt:
        break
    except:
        print('no illust')
        continue 
