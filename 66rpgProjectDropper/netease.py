import urllib3
import json
import base64
import re
import os
from pathlib import Path
import datetime
import hashlib
import requests
from bs4 import BeautifulSoup


print('https://avg.163.com/game/detail/12908 的id为12908')
game_id = input('请输入游戏id 默认12908：\n')

# 获取标题创建对应文件夹
if game_id == '':
    game_id = '12908'

fileMap = {}
# 获取游戏资源
game_url = 'https://avg.163.com/avg-portal-api/game/' + \
    game_id+'/config?gameID='+game_id
# https://a13.fp.ps.netease.com/
print('game_url', game_url)
file_server_url = 'https://a13.fp.ps.netease.com/file'
# md5 = '64539ae95a2098099542a5e1qOOVQuYi04'


http = urllib3.PoolManager()
headers = {
    # 'Host': 'avg.163.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.68',
    'sec-ch-ua-platform': 'Windows',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    # 这个属性很关键
    'Referer': 'https://avg.163.com/engine/?gameId=12908&t=1683257372209',
    'Cookie': 'WM_NI=r4OiQQ6Hqu14wYbvWkKKSIQvIvEuAJBOdVRiD%2Fw1XYQ5DOcdtoVMtGyAOQVqFcRdD0oyYlpFUxRZwiVjO29KTm7XEiHThZVUzGPuXKMGonD5QJIGBMyxszXAkhdGcPGWWUE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb9ed6baa8e9eacd842b5eb8aa2d14f838e9e82c548f5b6889bc146abe7bb96dc2af0fea7c3b92ab2ec818ad45bf698bf96b440b587ae97d66189959daad47e8baa8b96c4428291acb7d16388f1b9d2db5393eb8cb0e270b8b19aaef74dbb9f81b2d57b86bd9e85c73cada7978df34e97a89ebbf66396b681d3bc4198b3f9b9c8638c8ca8bbd55fba99a096db418f99a18fc73f939687a8c147bba8bd9bdb4ba9b8aca8e25c858999b6c837e2a3; WM_TID=A8Er3QmhklRABBBVFQfAa%2FnGnBcjo6%2BY; A13_SDK_TOKEN=975ffc90c71f1ffd8039be5e3bb53b41f26dcf9dae4b24c2779088af36c838fd57560d3d62f9a5a261c17bc7f730582026eaab090eca2dc943c8c7d9cfbbcba42da45cb5a5f24ff3b7532ee6c46b64f6cd5473fc08b8a8473af79f8f7533e31ae8b2c1107616bdb97fffd2a9018eae6e49dce6cc36fea1d04d20c2b3d647f93b807ab601d43238c812a35dffba68981d215caa2764021ef1ef3b05c86d218a724c0bf94a0a6c397d8badda5a534ac81e5abeae767fbbc3c324633bf0f1340a5f; TOKEN=9b17c9438bb5383b29ec93e9308bdda2; AVG_LOGIN_USER_ID=17882437; awwy_et=c1187b64082060fb99d1e443e33fd0abd34cd7098f717',
    # 'Cookie': '_ntes_nnid=bb4090daa2c3694dee1ac631e4ad77db,1645674058594; _ntes_nuid=bb4090daa2c3694dee1ac631e4ad77db; WM_TID=YGv%2FpQV1BD9BQFFBFBKQOvyCjG2xhe%2Fn; __bid_n=187e9b3a81bd5eb7b84207; A13_SDK_TOKEN=ab9486b43f849eaad0f4a7020446d771d6207220d604362cb21bf3034d22fa310fc146380bcf2da23baa16c7bac08b42a3b0b0a8ae7213e49ebf618bc950fc9a674c6fd91f1d206f427d286e3e131e2ee07fc80c9aa5c79e30923897bfd4887c846e17e9d77f48654d03dd9892f0d1c5571f2e6c2f1a0037fdd054d4f9acd1e43a46db0bb85f9e116af08e21a8d99cea114c01697b11d7f429638d075fd6200f; TOKEN=9b17c9438bb5383b29ec93e9308bdda2; AVG_LOGIN_USER_ID=17882437; timing_user_id=time_sOCt542tre; awwy_et=c1187eb3082061e85896fdbeb26956489b1d9b78c3c0d; WM_NI=B2xlT8oH1dWImkMl176Kmyn5ARJguW66bkxDxVtTLK%2FhX8fu10Qjxh0BTXglAJ2liRiy0zEMZbL6aTRRf9fenY1sjDuzP03MHuZwVfLAQzhTxNoQXzNtx4HfO87OSYeOeTI%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee96cc6aaab6f8d3c447a5eb8ab2c14e929f9aadd845b6b7a6cce65ab69585a3d52af0fea7c3b92a82eeb88dd734ad98ff85d643afb5838db43df695a39aed3f838e8688f85df6eaae8cfb50bc8abcb5cf41edb898d9e57ff3f09f8bfb64f49e9cb9e6688396fe8dec5aaba7009bc8479abe84d7e460928eaadae56fae87ff94e950b7a6a0d1b2478cab9698d56e909f9f9beb60bc92a1b2db728eacb8d5cb6e8de8f9b0d253a791abb5cc37e2a3',
}
json_str = ''

# 获取游戏数据


def write_file(file, data):
    if os.path.exists(file):
        print(file, '已存在')
        return
    filepathIndex = file.rfind('/')
    dir = file[:filepathIndex]
    if not os.path.exists(Path(dir)):
        os.makedirs(Path(dir))

    if isinstance(data, str):
        data = data.encode('utf-8').decode('utf-8')
        f = open(file,  mode='w', encoding='utf-8')
        f.write(data)
        f.close()
    if isinstance(data, bytes):
        f = open(file, mode='wb')
        f.write(data)
        f.close()
    print('正在写入', file)


def get_netease_data(url: str):
    req = http.request('GET', url, headers=headers)
    jsonstr = req.data.decode('utf-8')
    # print('str',jsonstr)
    obj = json.loads(jsonstr)
    # print('obj::\n\n', url)
    res = json.loads(obj['data']['data'])
    return res


game_data = get_netease_data(game_url)
# 标题
title = game_data['game']['name']
# 游戏目录
game_dir = os.path.dirname(__file__) + '/../download/' + game_id + '_' + title

# 保存源剧本
# fileMap[game_dir+'/game_data.json'] = json.dumps(game_data)
write_file(game_dir+'/game_data.json', json.dumps(game_data))

# https://avg.163.com/avg-portal-api/game/12908/config/scene/151052?em=1
print('开始下载')
if not os.path.exists(game_dir):
    os.makedirs(game_dir)
    # 打印文件夹名称
    print("Folder created:", game_dir)

whole_scene_text = ''

# 文件写入


def get_attr(obj: dict, attr: str):
    arr = attr.split('.')
    while len(arr) > 0:
        if arr[0] in obj:
            obj = obj[arr.pop(0)]
        else:
            return None
    return obj


resourcesMap = {}


def get_scenes(json_obj):
    # print('get_scenes')
    if len(json_obj) > 0:
        for chapter in json_obj:
            if 'scenes' in chapter and len(chapter['scenes']) > 0:
                for scene in chapter['scenes']:
                    name = scene['name']
                    id = scene['id']
                    # 章节源文件
                    scene_dir = game_dir + '/scenes/' + str(id)+"_"+name
                    key = scene_dir + '/scene_data.json'
                    scene_url = 'https://avg.163.com/avg-portal-api/game/'+str(game_id)+'/config/scene/' + \
                        str(id)
                    scene_data = get_netease_data(scene_url)
                    fileMap[key] = json.dumps(scene_data)

                    if 'resource' in scene_data:
                        # 图片
                        for key in scene_data['resource']['image']:
                            image = scene_data['resource']['image'][key]
                            # print('image',image,value)
                            name = image['name']
                            fileType = image.get('fileType')
                            if fileType == None:
                                fileType = 'png'
                            url = image['url']
                            resourcesMap[game_dir+'/image/' +
                                         name+'.'+fileType.lower()] = url
                        # 字体
                        for key in scene_data['resource']['fontFamilies']:
                            fontFamilies = scene_data['resource']['fontFamilies'][key]
                            # print('fontFamilies',fontFamilies,value)
                            name = fontFamilies['fontName']
                            fileType = 'ttf'
                            # try:
                            url = None
                            # first_key = next(iter(fontFamilies['files'].keys()))
                            if url == None:
                                url = get_attr(
                                    fontFamilies, 'files.simplified.ttf')
                            if url == None:
                                url = get_attr(
                                    fontFamilies, 'files.complete.ttf')
                            if url == None:
                                url = get_attr(
                                    fontFamilies, 'files.gameFont.ttf')
                            if url != None:
                                resourcesMap[game_dir+'/fontFamilies/' +
                                             name+'.'+fileType.lower()] = url
                        # 音频
                        for key in scene_data['resource']['audio']:
                            audio = scene_data['resource']['audio'][key]
                            # print('audio',audio,value)
                            name = audio['name']
                            fileType = image.get('fileType')
                            if fileType == None:
                                fileType = 'mp3'
                            url = audio['url']
                            resourcesMap[game_dir+'/audio/' +
                                         name+'.'+fileType.lower()] = url

                    # 章节纯剧本
                    cmd_list = scene_data['commands']
                    d = ''.join([
                        s for s in cmd_list
                        if True
                        # not s.startswith('[')
                        and not s.startswith('[async]')
                        and not s.startswith('[endasync]')
                        and not s.startswith('[sync]')
                        and not s.startswith('[endsync]')
                        and not s.startswith('image ')
                        and not s.startswith('show ')
                        and not s.startswith('callMacro ')
                        and not s.startswith('callUI ')
                        and not s.startswith('playAudio ')
                        and not s.startswith('stopAudio ')
                        and not s.startswith('remove ')
                        and not s.startswith('callMacro ')
                        # and not s.startswith('text ')
                        and not s.startswith('style ')
                        and not s.startswith('shakeScreen ')
                        and not s.startswith('trans ')
                        # and not s.startswith('textOptionGroup ')
                        and not s.startswith('blocked;')
                        and not s.startswith('delay ')
                    ])

                    fileMap[scene_dir + '/剧本.txt'] = d
                    global whole_scene_text
                    whole_scene_text = whole_scene_text + '\n------------------------- plotID:' + \
                        str(id)+" "+"剧情:"+name+' --------------------------\n'+d + \
                        '\n##########################################################\n'

            if 'sections' in chapter and len(chapter['sections']) > 0:
                get_scenes(chapter['sections'])


get_scenes(game_data['chapters'])


fileMap[game_dir+'/剧本合并.txt'] = whole_scene_text

for key, value in fileMap.items():
    write_file(key, value)
print('剧情数据下载完毕...')

count = 0
length = len(resourcesMap)
print('资源下载进度'+str(count / length * 100)+'%')
for path, url in resourcesMap.items():
    write_file(path, http.request('GET', url=url, headers=headers).data)
    count += 1
    print('资源下载进度'+str(count / length * 100)+'%')
print('资源下载完毕...')


# print(filtered_list)


print('爬取完成')
