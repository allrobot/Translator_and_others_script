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

def disguise_file(src_file: str, video_file: str, out_file: str = None):
    """
    把 src_file 伪装到 video_file 中，生成新的伪装视频
    """
    if not os.path.exists(src_file):
        print(f"要伪装的文件不存在: {src_file}")
        return 0
    if not os.path.exists(video_file):
        print(f"伪装用的视频文件不存在: {video_file}")
        return 0

    if out_file is None:
        out_file = os.path.join(
            os.path.dirname(src_file),
            os.path.basename(video_file)
        )

    # 假如目标视频文件已存在
    if os.path.exists(out_file):
        out_file = get_unique_filename(out_file)

    # 1. 先复制视频
    __import__("shutil").copy(video_file, out_file)

    # 2. 准备元数据
    src_size = os.path.getsize(src_file)
    video_size = os.path.getsize(out_file)
    meta = {
        "src_name": os.path.basename(src_file),
        "src_size": src_size,
        "video_size": video_size,
        "xor_key": XOR_KEY
    }
    meta_bytes = json.dumps(meta).encode("utf-8")
    meta_len = len(meta_bytes)

    # 3. 写入混淆后的原始文件 + 元数据 + 签名 + 元数据长度
    with open(out_file, "ab") as f_out, open(src_file, "rb") as f_src:
        # 混淆写入原始文件
        while chunk := f_src.read(1024 * 1024):
            f_out.write(bytes([b ^ XOR_KEY for b in chunk]))
        # 写入元数据
        f_out.write(meta_bytes)
        # 写入签名
        f_out.write(MAGIC)
        # 写入元数据长度
        f_out.write(struct.pack("<Q", meta_len))

    send2trash(src_file)
    print(f"✅ 伪装完成: {out_file}  (原文件 {src_file} 大小: {src_size / 1024 / 1024:.2f} MB -> {os.path.getsize(out_file)/1024/1024:.2f} MB)")


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
    print("加密、解密脚本工具")
    print("=" * 50)

    conti_ = ''
    video_folder = r'cover_video'
    if not os.path.exists(video_folder):
        print(f'# 未找到cover_video文件夹，请在脚本所在路径新建一个cover_video文件夹，并放入多个 mp4 视频文件')
        print(f'\n# 此时只能解密文件，是否继续？')
        conti_ = input(f'输入（y/n）：')
        while True:
            if conti_ == 'y':
                break
            elif conti_ == 'n':
                exit(0)
            else:
                '无效命令'

    # 初始获取目标目录
    target_dir = input("请输入要处理的目录路径: ").strip('"\' ')

    try:
        while True:
            if not os.path.exists(target_dir):
                print(f"错误：目录 '{target_dir}' 不存在")
                target_dir = input("请重新输入要处理的目录路径: ").strip('"\' ')
                continue

            print(f"\n当前目录: {target_dir}")
            print("\n请选择操作:")
            print("1. 退出")
            print("2. 重新选择目录")
            if conti_ == 'y':
                pass
            elif conti_ == '':
                print("3. 将目标文件夹内的所有文件加密并伪装为视频")
                if os.listdir(video_folder).__len__() < os.listdir(target_dir).__len__():
                    print(
                        f"\n# 提示：cover_video 文件夹中的视频数量少于目标文件夹中的文件数量。\n# 请补充视频文件，建议与需要加密的文件数量保持一致，或放更多的 mp4 视频。")
                    print(f"# cover_video文件夹路径为 {os.getcwd()}\\{video_folder}\n")
            print("4. 还原目标文件夹内的所有 mp4 文件")

            choice = input("请输入选项 (1-4): ").strip()

            if choice == "1":
                print("退出程序")
                break
            elif choice == "2":
                new_dir = input("请输入新的目录路径: ").strip('"\' ')
                if os.path.exists(new_dir):
                    target_dir = new_dir
                    print(f"已切换到目录: {target_dir}")
                else:
                    print(f"错误：目录 '{new_dir}' 不存在")
            elif choice == "3":
                if conti_ == '':
                    video_list = sorted(os.listdir(video_folder),
                                        key=lambda x: [int(text) if text.isdigit() else text.lower()
                                                       for text in re.split(r'(\d+)', x)])
                    index = 0
                    for file in os.listdir(target_dir):
                        index += 1
                        if index > video_list.__len__():
                            print(
                                f'# 如果用于伪装的视频数量少于需要加密的文件数量，可能会引起怀疑。\n# 当前将循环使用视频进行伪装，但建议最好准备足够数量的视频文件，以提升伪装效果。  ')
                            index = 0
                        if video_list.__len__() == 0:
                            print(f'cover_video文件夹没有伪装视频，无法加密')
                        else:
                            file_path = os.path.join(target_dir, file)
                            video_path = os.path.join(video_folder, video_list[index - 1])
                            # print(video_path)
                            # stream = os.popen('where ffmpeg')
                            # output = stream.buffer.read().decode('utf-8', errors='ignore')
                            # print(output)
                            try:
                                disguise_file(file_path, video_path)

                            except:
                                print(f'加密异常，请检查文件：{file_path}\n错误报告：{traceback.format_exc()}')
                else:
                    print("无效选项，请重新选择")

            elif choice == "4":
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
                    print(f'目标路径不存在mp4文件')

            else:
                print("无效选项，请重新选择")
            print('=' * 80)
    except Exception as e:
        print(traceback.format_exc())
        input("按下回车自动退出")


if __name__ == "__main__":
    main_menu()
