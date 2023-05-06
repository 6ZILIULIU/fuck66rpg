import struct
import sys
from pathlib import Path

game_dir = sys.argv[1]
game_dir_path = Path(game_dir)
print('game_dir',game_dir)
# 打开二进制文件
with open(game_dir, 'rb') as f:
    # 打开写入文件
    with open('convertToIn32.txt', 'w', encoding='utf-8') as f_out:
        # 读取文件中所有数据
        while True:
            # 读取4个字节（即一个Int32）的数据
            data = f.read(4)
            if not data:
                # 如果读取完毕，退出循环
                break
            # 将读取的二进制数据转换为Int32
            print('f:',data)
            int_data = struct.unpack('i', data)[0]
            # 将Int32转换为UTF-8编码，并写入到文件中
            f_out.write(str(int_data) + '\n')