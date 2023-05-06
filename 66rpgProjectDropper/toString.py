
import unicodedata
import sys
import re
import base64
from pathlib import Path
import openpyxl

game_dir = sys.argv[1]
game_dir_path = Path(game_dir)


def remove_non_unicode(text):
    return ''.join(c for c in text if unicodedata.category(c)[0] != 'C')


def replace_non_unicode(text):
    return ''.join(c if unicodedata.category(c)[0] != 'C' else ';' for c in text)


game1 = "E:/myCode/fuck66rpg/（区半+挂件）今夜与深渊有约/data/Game.bin"
game2 = "E:/myCode/fuck66rpg/重生天后进化论/data/Game.bin"
print('game_dir', game_dir+"/"+'剧本.xlsx')

with open(game_dir+'/data/Game.bin', 'rb') as intput_f, \
        open(game_dir+'/剧本src.txt', 'w', encoding='utf-8') as output_f2, \
        open(game_dir+'/剧本hex.txt', 'w', encoding='utf-8') as output_f3, \
        open(game_dir+'/剧本.txt', 'a', encoding='utf-8') as output_f:
    binary_data = intput_f.read()
    encoding = 'utf-8'

    # mapbinHex = base64.b16encode(binary_data).decode()
    # mapbinHex = mapbinHex[16:]  # 切掉文件头
    # mapbinHex = mapbinHex[:26] + "0D0A" + mapbinHex[42:] # 切掉文件头
    # # 分割文件名和MD5，并保证后半部分剩余的hex不是奇数。否则 X[X XX XX X0 02 00 00 00 0]X 会匹配错误
    # mapbinHex = re.sub('......0020000000(?!.(..)*$)', '0D0A', mapbinHex)
    # mapbinHex = re.sub('..000000(?!.(..)*$)', '0D0A', mapbinHex)  # 分割行，并保证后半部分剩余的hex数据不是奇数。理由同上。

    # mapbinUTF8 = base64.b16decode(mapbinHex.encode()).decode('UTF-8')
    # # mapbinUTF8 = str.split(mapbinUTF8, '\r\n')
    # output_f3.write(mapbinUTF8)


    string_data = binary_data.decode(encoding, errors='ignore')
    string_data = replace_non_unicode(string_data)
    data_arr = string_data.split(';')
    string_data = '\n;'.join(data_arr)
    output_f2.write(string_data)

    # 找到|d后 15行是人名 19行是颜色 22行是对话
    talk_tag_str = "d"
    talk_tag_str = "e"
    # 标志位，表示是否开始写入
    talk_flag = False
    switch_flag = False
    # 计数器，记录已经数过的行数
    count = 0
    # 遍历原始文件的每一行
    output_f.truncate(0)

    # 创建一个新的 Excel 文件
    workbook = openpyxl.Workbook()
    # 获取默认的工作表（Sheet）
    sheet = workbook.active
    # sheet.append(["行数", "角色", "对话"])
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
            sheet.append(["分支条件", "", line])
        if "的剧情" in line:
            output_f.write("\n"+line)
            sheet.append(["分支剧情", "", line])

        # 判断是否包含目标字符串
        if "d" == line:
            # print('line 1',target_string, line)
            # 设置标志位为True，表示开始写入
            role = data_arr[idx+15]
            # if not role:
            #     role = "我:"
            color = data_arr[idx+19]
            talk = data_arr[idx+22] + '  ' + data_arr[idx+23]
            # print('talk',talk)
            res = "" + ("\n") + str("对话:").ljust(8, " ") + \
                (" ") + role.ljust(8, " ") + talk
            # 向工作表写入数据
            # data = [['姓名', '年龄', '性别'],
            #         ['张三', 25, '男'],
            #         ['李四', 30, '男'],
            #         ['王五', 28, '女']]
            # if talk or role:
            sheet.append([idx, role, talk])
            output_f.write(res)
            # talk_flag = True
            # output_f.write(idx+":"+line)
        # 判断是否包含目标字符串
        if "e" == line:
            # print('line 1',target_string, line)
            # 设置标志位为True，表示开始写入
            role = "<选项:>"
            talk = ""
            talk += "\n  >>> :["+data_arr[idx+15]+"]"
            talk += "\n  >>> :["+data_arr[idx+19]+"]"
            res = "" + ("\n") + str(idx).ljust(8, " ") + \
                (" ") + role.ljust(8, " ") + talk
            # 向工作表写入数据
            # data = [['姓名', '年龄', '性别'],
            #         ['张三', 25, '男'],
            #         ['李四', 30, '男'],
            #         ['王五', 28, '女']]
            # if talk or role:
            sheet.append([idx, role, talk])
            output_f.write(res)
    # 保存 Excel 文件
    print(game_dir+'/剧本.xlsx')
    workbook.save(game_dir+'/剧本.xlsx')


# lines = string_data.splitlines()
# for line in lines:
#     if "礼包" not in line:
#         f.write(line)
# 在窗口上显示一些文本，提示用户输入
print("请按任意键继续...")
# 等待用户输入
input()
