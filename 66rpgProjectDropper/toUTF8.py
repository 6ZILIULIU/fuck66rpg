import urllib3
import json
import base64
import re
import os
from pathlib import Path
import datetime
import hashlib
import hmac

import unicodedata


    
lj = "E:/myCode/fuck66rpg/1563726_区半商半800W福利·娱乐掌门人/Map2.txt"
lj2 = "E:/myCode/fuck66rpg/1563726_区半商半800W福利·娱乐掌门人/Map3.txt"
with open(lj,'rb') as f,open(lj2,'w') as f2:
    data = f.read()
    mapbinUTF8 = base64.b16decode(data).decode('UTF-8')
    # mapbinUTF8 = str.split(mapbinUTF8, '\r\n')
    f2.write(mapbinUTF8)
os._exit(0)
# 分割文件名和MD5，并保证后半部分剩余的hex不是奇数。否则 X[X XX XX X0 02 00 00 00 0]X 会匹配错误
mapbinHex = re.sub('......0020000000(?!.(..)*$)', '0D0A', mapbinHex)
# 分割行，并保证后半部分剩余的hex数据不是奇数。理由同上。
mapbinHex = re.sub('..000000(?!.(..)*$)', '0D0A', mapbinHex)
mapbinUTF8 = base64.b16decode(mapbinHex.encode()).decode('UTF-8')
mapbinUTF8 = str.split(mapbinUTF8, '\r\n')
# print('mapbinHex 1',mapbinUTF8)
lowercasefileName = mapbinUTF8[::2]  # 取偶数项
MD5 = mapbinUTF8[1::2]  # 取奇数项

# # 更正fileName大小写
# fileName = []
# for name in lowercasefileName:
#     print(';fileName',name)
#     name = name.replace('audio/bgm/', 'Audio/BGM/')
#     name = name.replace('audio/se/', 'Audio/SE/')
#     name = name.replace('audio/voice/', 'Audio/Voice/')
#     name = name.replace('audio/bgs/', 'Audio/BGS/1')
#     # name = name.replace('data/game.bin', 'Data/Game.bin')
#     name = name.replace('data/game.bin', 'data/Game.bin')
#     name = name.replace('data/project.bin', 'data/Project.bin')
#     # name = name.replace('data/map.bin', 'Data/Map.bin')
#     name = name.replace('data/map.bin', 'data/Map.bin')
#     name = name.replace('font/', 'Font/')
#     name = name.replace('graphics/background/', 'Graphics/Background/')
#     name = name.replace('graphics/button/', 'Graphics/Button/')
#     name = name.replace('graphics/face/', 'Graphics/Face/')
#     name = name.replace('graphics/half/', 'Graphics/Half/')
#     name = name.replace('graphics/mood/', 'Graphics/Mood/')
#     name = name.replace('graphics/other/', 'Graphics/Other/')
#     name = name.replace('graphics/system/', 'Graphics/System/')
#     name = name.replace('graphics/transitions/', 'Graphics/Transitions/')
#     name = name.replace('graphics/ui/', 'Graphics/UI/')
#     name = name.replace('graphics/chat/', 'Graphics/Chat/')
#     name = name.replace('graphics/oafs/', 'Graphics/Oafs/')
#     fileName.append(name)

# filePath = []  # 提出文件路径用于创建文件夹
# for a in fileName:
#     filepathIndex = a.rfind('/')
#     filePath.append(a[:filepathIndex])

# 下载素材文件
# http://wcdn1.cgyouxi.com/shareres/$md5前两位$/$md5$
# 网页客户端的CDN为，似乎都可以使用
# https://dlcdn1.cgyouxi.com/shareres/$md5前两位$/$md5$
# for i in range(len(fileName)):
#     print(Path(gameName + '/' + fileName[i]), MD5[i])
#     file = http.request('GET', 'http://wcdn1.cgyouxi.com/shareres/' + MD5[i][:2] + '/' + MD5[i]).data
#     isExists = os.path.exists(Path(gameName + '/' + filePath[i]))
#     if not isExists:  # 判断如果文件不存在,则创建
#         os.makedirs(Path(gameName + '/' + filePath[i]))
#     f = open(Path(gameName + '/' + fileName[i]), mode='wb')
#     f.write(file)
#     f.close()

# print('素材文件下载完成')

os._exit(0)

# print('开始解析Game.bin')
# def remove_non_unicode(text):
#     return ''.join(c for c in text if unicodedata.category(c)[0] != 'C')


# def replace_non_unicode(text):
#     return ''.join(c if unicodedata.category(c)[0] != 'C' else '|' for c in text)

# with open(Path(gameName+'/'+'data/Game.bin', 'rb')) as f:
#     binary_data = f.read()
#     encoding = 'utf-8'
#     string_data = binary_data.decode(encoding, errors='ignore')


# print('完成解析Game.bin')


print('准备下载工程文件')

# 工程文件储存在阿里云OSS中
# 隐藏在「other/StoryNew[0-9].data」、「other/Story[0-9].data」、「bin/Story.bin」这21个文件中
# 下载地址为
# http://ouser.oss.aliyuncs.com/$uid$/$guid$/$projectfilePath$
# 请求方式GET，请求头示例为
'''
GET /$uid$/$guid$/$projectfilePath$ HTTP/1.1
Host: ouser.oss.aliyuncs.com
Date: Mon, 27 Jul 2020 10:20:37 GMT
Authorization: OSS uEwcePgrON2VXsbv:$sign$
'''
OSS_ACCESS_KEY = "uEwcePgrON2VXsbv"
ACCESS_SECRET = "GHsIlajWNEkiF2QoJyrpq1rmx2uwLs"
HOST = "ouser.oss.aliyuncs.com"
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

for i in range(11):
    for story in ['StoryNew', 'Story']:
        if i == 10:
            projectfilePath = 'bin/Story.bin'
        else:
            projectfilePath = 'other/' + story + str(i) + '.data'
        url = 'http://' + HOST + '/' + uid + '/' + guid + '/' + projectfilePath

        # 开始制作sign
        # sign为「GET\n\n\n$GMT$\n/ouser/$uid$/$guid$/$projectgamePath$」的HMAC-SHA1加密
        signInvalid = True
        while signInvalid:
            GMT = datetime.datetime.utcnow().strftime(GMT_FORMAT)  # 生成GMT时间
            signData = 'GET\n\n\n' + GMT + '\n/ouser/' + \
                uid + '/' + guid + '/' + projectfilePath
            # 计算HMACsign
            key = bytes(ACCESS_SECRET, 'UTF-8')
            message = bytes(signData, 'UTF-8')
            digester = hmac.new(key, message, hashlib.sha1)
            signature1 = digester.digest()
            signature2 = base64.urlsafe_b64encode(signature1)
            sign = str(signature2, 'UTF-8')
            if '_' not in sign and '-' not in sign:  # 阿里云oss规定sign中不能含有-和_
                signInvalid = False

        headers = {
            'Host': HOST,
            'Date': GMT,
            'Authorization': 'OSS ' + OSS_ACCESS_KEY + ':' + sign
        }
        respone = http.request('GET', url, None, headers)
        if respone.status == 200:
            # isExists = os.path.exists(Path(gameName + '/Data'))
            # if not isExists:
            #    os.makedirs(Path(gameName + '/Data'))

            # f = open(Path(gameName + '/Data/Story.data'), mode='wb')
            # f.write(respone.data)
            f = open(Path(gameName + '/Data/StoryNew.data'), mode='wb')
            f.write(respone.data)
            # f = open(Path(gameName + '/avgEditor.avgmakerO'), mode='w')
            # f.write('')
            f = open(Path(gameName + '/avgEditor.avgmakerONew'), mode='w')
            f.write('')
            print(projectfilePath + ' ' + str(respone.status) + ' 工程文件下载成功！')
            os._exit(0)

        else:
            print(projectfilePath + ' ' + str(respone.status) + ' 文件获取失败')
            if i == 10:
                print('服务器中未找到工程文件，旧版工程可以尝试逆向Game.bin')
                os._exit(0)
