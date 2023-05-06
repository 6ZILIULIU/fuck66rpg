import unicodedata
import sys
import re
import os
import base64
from pathlib import Path
import openpyxl

game_dir = sys.argv[1]
game_dir_path = Path(game_dir)

game1 = "E:/myCode/fuck66rpg/（区半+挂件）今夜与深渊有约/data/Game.bin"
game2 = "E:/myCode/fuck66rpg/重生天后进化论/data/Game.bin"
print('game_dir', game_dir+"/"+'剧本.xlsx')

with open(game_dir+'/data/Game.bin', 'rb') as intput_f, \
        open(game_dir+'/analysis.txt', 'a', encoding='utf-8') as output_f3:
        # open(game_dir+'/剧本src.txt', 'w', encoding='utf-8') as output_f2, \
        # open(game_dir+'/剧本.txt', 'a', encoding='utf-8') as output_f:
    binary_data = intput_f.read()
    encoding = 'utf-8'
    mapbinHex = base64.b16encode(binary_data).decode()
    # mapbinHex = mapbinHex[32*7:]  # 切掉文件头
    
    print('------------------ 1',len(mapbinHex))
    # mapbinHex = mapbinHex[:26] + "0D0A" + mapbinHex[42:] # 切掉文件头
    # 分割文件名和MD5，并保证后半部分剩余的hex不是奇数。否则 X[X XX XX X0 02 00 00 00 0]X 会匹配错误
    # mapbinHex = re.sub('000000..(?!.(..)*$)', '0D0A', mapbinHex)  # 分割行，并保证后半部分剩余的hex数据不是奇数。理由同上。
    # mapbinHex = re.sub('0000000000000000(?!.(..)*$)', '0D0A', mapbinHex)  # 分割行，并保证后半部分剩余的hex数据不是奇数。理由同上。
    output_f3.truncate(0)
    cur_list = []
    while len(mapbinHex):
        # cur_list.append(mapbinHex[:5])
        output_f3.write('\n'+mapbinHex[:4])
        mapbinHex = mapbinHex[4:]
        print('len(mapbinHex)',len(mapbinHex))
    print('------------------ 2')
    # mapbinUTF8 = base64.b16decode(mapbinHex.encode()).decode('UTF-8')
    # mapbinUTF8 = str.split(mapbinUTF8, '\r\n')
    # mapbinHex = str.split(mapbinHex, '0D0A')
    # for v in cur_list:
    #     # print('------------------ 3',v)
    #     output_f3.write('\n'+v)
    # string_data = mapbinUTF8.decode(encoding, errors='ignore')
    # 只留下中文
    '''
    # pattern = re.compile(r'[\u4e00-\u9fa5\:a-zA-Z]+')  # 匹配中文字符和逗号的正则表达式
    # string_data = ''.join(pattern.findall(string_data))

    # string_data = string_data.replace('数值：', '\n数值：')
    # string_data = string_data.replace('高级条件分歧', '\n高级条件分歧:')
    data_arr = string_data.split('#')
    # data_arr = [item for item in data_arr if item is not None and item != '' and item != [] and item != {}]
    string_data = '\n#'.join(data_arr)
    output_f2.write(string_data)

    # 找到|d后 15行是人名 19行是颜色 22行是对话
    target_string = "d"
    # 标志位，表示是否开始写入
    write_flag = False
    # 计数器，记录已经数过的行数
    count = 0
    # 遍历原始文件的每一行
    output_f.truncate(0)

    # 创建一个新的 Excel 文件
    workbook = openpyxl.Workbook()
    # 获取默认的工作表（Sheet）
    sheet = workbook.active
    sheet.append(["行数", "角色", "对话"])
    # print('清空完毕')
    
    role = ""
    talk = ""
    for idx, line in enumerate(data_arr):
        # idx = index
        # line = value
        # print(idx,line)
        # print('遍历',line)
        # 如果标志位为True，表示已经找到目标字符串并开始写入
        if "高级条件分歧:" in line:
            output_f.write("\n"+line)
            sheet.append(["分支", "", line])

        if write_flag:
            # 增加计数器
            count += 1

            # 如果计数器达到22，表示已经数过22行
            if count == 15:
                # print('line 2', line)
                # output_f.write("\n"+str(idx)+":"+line)
                role = line
            elif count == 22:
                # 重置计数器
                # 将当前行写入新文件
                # print('line 3', line)

                talk = line
                res = "" + ("\n") + str(idx).ljust(8, " ") + \
                    (" ") + role.ljust(8, " ") + talk
                # 向工作表写入数据
                # data = [['姓名', '年龄', '性别'],
                #         ['张三', 25, '男'],
                #         ['李四', 30, '男'],
                #         ['王五', 28, '女']]
                if talk or role:
                    sheet.append([idx, role, talk])
                    output_f.write(res)

                count = 0
                write_flag = False
                role = ""
                talk = ""
            else:
                # 继续循环下一行
                continue

        # 判断是否包含目标字符串
        if target_string == line:
            # print('line 1',target_string, line)
            # 设置标志位为True，表示开始写入
            write_flag = True
            # output_f.write(idx+":"+line)

    # 保存 Excel 文件
    workbook.save(game_dir+'剧本.xlsx')


# lines = string_data.splitlines()
# for line in lines:
#     if "礼包" not in line:
#         f.write(line)
# 在窗口上显示一些文本，提示用户输入
print("请按任意键继续...")
# 等待用户输入
input()
'''
'''
备份 原始导出
0000003010000000

import unicodedata
import sys
import re
from pathlib import Path
import openpyxl

game_dir = sys.argv[1]
game_dir_path = Path(game_dir)


def remove_non_unicode(text):
    return ''.join(c for c in text if unicodedata.category(c)[0] != 'C')


def replace_non_unicode(text):
    return ''.join(c if unicodedata.category(c)[0] != 'C' else '#' for c in text)


game1 = "E:/myCode/fuck66rpg/（区半+挂件）今夜与深渊有约/data/Game.bin"
game2 = "E:/myCode/fuck66rpg/重生天后进化论/data/Game.bin"
print('game_dir', game_dir+"/"+'剧本.xlsx')

with open(game_dir+'/data/Game.bin', 'rb') as intput_f, \
        open(game_dir+'/剧本src.txt', 'w', encoding='utf-8') as output_f2, \
        open(game_dir+'/剧本.txt', 'a', encoding='utf-8') as output_f:
    binary_data = intput_f.read()
    encoding = 'utf-8'

    string_data = binary_data.decode(encoding, errors='ignore')
    string_data = replace_non_unicode(string_data)

    # 只留下中文
    # pattern = re.compile(r'[\u4e00-\u9fa5\:a-zA-Z]+')  # 匹配中文字符和逗号的正则表达式
    # string_data = ''.join(pattern.findall(string_data))

    # string_data = string_data.replace('数值：', '\n数值：')
    # string_data = string_data.replace('高级条件分歧', '\n高级条件分歧:')
    data_arr = string_data.split('#')
    # data_arr = [item for item in data_arr if item is not None and item != '' and item != [] and item != {}]
    string_data = '\n#'.join(data_arr)
    output_f2.write(string_data)

    # 找到|d后 15行是人名 19行是颜色 22行是对话
    target_string = "d"
    # 标志位，表示是否开始写入
    write_flag = False
    # 计数器，记录已经数过的行数
    count = 0
    # 遍历原始文件的每一行
    output_f.truncate(0)

    # 创建一个新的 Excel 文件
    workbook = openpyxl.Workbook()
    # 获取默认的工作表（Sheet）
    sheet = workbook.active
    sheet.append(["行数", "角色", "对话"])
    # print('清空完毕')
    
    role = ""
    talk = ""
    for idx, line in enumerate(data_arr):
        # idx = index
        # line = value
        # print(idx,line)
        # print('遍历',line)
        # 如果标志位为True，表示已经找到目标字符串并开始写入
        if "高级条件分歧:" in line:
            output_f.write("\n"+line)
            sheet.append(["分支", "", line])

        if write_flag:
            # 增加计数器
            count += 1

            # 如果计数器达到22，表示已经数过22行
            if count == 15:
                # print('line 2', line)
                # output_f.write("\n"+str(idx)+":"+line)
                role = line
            elif count == 22:
                # 重置计数器
                # 将当前行写入新文件
                # print('line 3', line)

                talk = line
                res = "" + ("\n") + str(idx).ljust(8, " ") + \
                    (" ") + role.ljust(8, " ") + talk
                # 向工作表写入数据
                # data = [['姓名', '年龄', '性别'],
                #         ['张三', 25, '男'],
                #         ['李四', 30, '男'],
                #         ['王五', 28, '女']]
                if talk or role:
                    sheet.append([idx, role, talk])
                    output_f.write(res)

                count = 0
                write_flag = False
                role = ""
                talk = ""
            else:
                # 继续循环下一行
                continue

        # 判断是否包含目标字符串
        if target_string == line:
            # print('line 1',target_string, line)
            # 设置标志位为True，表示开始写入
            write_flag = True
            # output_f.write(idx+":"+line)

    # 保存 Excel 文件
    workbook.save(game_dir+'剧本.xlsx')


# lines = string_data.splitlines()
# for line in lines:
#     if "礼包" not in line:
#         f.write(line)
# 在窗口上显示一些文本，提示用户输入
print("请按任意键继续...")
# 等待用户输入
input()


'''