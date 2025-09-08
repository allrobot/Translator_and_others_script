import os
import json
import struct
import subprocess
import traceback
import re
from send2trash import send2trash

MAGIC = b'FAKEVID1'
LEN_SIZE = 8
XOR_KEY = 0xA7  # 混淆用的密钥，随便改


def extract_file(fake_video: str, out_dir: str = None):
    """
    从伪装视频中还原原始文件
    """
    if not os.path.exists(fake_video):
        print(f"伪装视频不存在: {fake_video}")
        return 0

    file_size = os.path.getsize(fake_video)

    with open(fake_video, "rb") as f:
        # 1. 读取元数据长度
        f.seek(file_size - LEN_SIZE)
        meta_len = struct.unpack("<Q", f.read(LEN_SIZE))[0]

        # 2. 检查签名
        sig_pos = file_size - LEN_SIZE - len(MAGIC)
        f.seek(sig_pos)
        magic = f.read(len(MAGIC))
        if magic != MAGIC:
            print("该文件不是伪装视频，无法还原")
            return 0

        # 3. 读取元数据
        meta_pos = sig_pos - meta_len
        f.seek(meta_pos)
        meta_bytes = f.read(meta_len)
        meta = json.loads(meta_bytes.decode("utf-8"))

        src_name = meta["src_name"]
        src_size = meta["src_size"]
        video_size = meta["video_size"]
        xor_key = meta.get("xor_key", XOR_KEY)

        # 4. 确定输出路径
        if out_dir is None:
            out_dir = os.path.dirname(fake_video)
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, src_name)

        # 假如目标文件已存在
        if os.path.exists(out_file):
            out_file = get_unique_filename(out_file)

        # 5. 解混淆原始文件
        f.seek(video_size)
        remaining = src_size
        with open(out_file, "wb") as f_out:
            while remaining > 0:
                chunk = f.read(min(1024 * 1024, remaining))
                if not chunk:
                    break
                f_out.write(bytes([b ^ xor_key for b in chunk]))
                remaining -= len(chunk)
    send2trash(fake_video)

    print(f"✅ 还原完成: {out_file}  (大小: {src_size / 1024 / 1024:.2f} MB)")
    return out_file


def get_unique_filename(out_file: str) -> str:
    """
    如果文件已存在，则自动在文件名后添加 -(n)，直到找到一个不存在的文件名。
    """
    # 拆分路径、文件名、扩展名
    dir_name = os.path.dirname(out_file)
    base_name = os.path.basename(out_file)
    name, ext = os.path.splitext(base_name)

    # 正则匹配类似 "xxx-(1)" 这种情况
    pattern = r"^(.*?)-\((\d+)\)$"
    match = re.match(pattern, name)

    if match:
        # 已经带有 -(n)
        base = match.group(1)
        counter = int(match.group(2))
    else:
        # 没有编号
        base = name
        counter = 0

    out_str = out_file
    while os.path.exists(out_str):
        counter += 1
        new_name = f"{base}-({counter}){ext}"
        out_str = os.path.join(dir_name, new_name)

    return out_str


def main_menu():
    """主菜单"""
    print("=" * 50)
    print("解密脚本工具")
    print("=" * 50)

    # 初始获取目标目录
    target_dir = os.getcwd()

    try:
        empty = 0
        for file in os.listdir(target_dir):
            fpath = os.path.join(target_dir, file)
            if os.path.isfile(fpath) and fpath.lower().endswith('.mp4'):
                print(f"🔹 还原文件: {file}")
                try:
                    extract_file(fpath)

                except:
                    print(f'解码异常，请检查文件：{fpath}\n错误报告：{traceback.format_exc()}')
            else:
                empty += 1
        if empty == os.listdir(target_dir).__len__():
            print(f'脚本当前路径不存在mp4文件')
    except Exception as e:
        print(traceback.format_exc())
        input("按下回车自动退出")


if __name__ == "__main__":
    main_menu()
