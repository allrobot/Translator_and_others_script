# -*- coding:utf-8
import os,json

import sys

import os
import subprocess

def process_lsb_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".lsb"):
                lsb_file = os.path.join(root, file)
                txt_file = os.path.splitext(lsb_file)[0] + ".txt"
                cmd = f"lmlsb dump \"{lsb_file}\" > \"{txt_file}\""
                print("执行命令：",cmd)
                subprocess.run(cmd, shell=True)

# 指定目录路径
while True:
    directory_path = input("\n执行lsb转为txt文件命令，请输入目录路径：\n")
    if os.path.exists(directory_path):
        break
    else:
        if os.path.exists(os.path.join(os.path.dirname(os.getcwd()),directory_path)):
            break
        else:
            print("\n目标路径并不存在！！！")

process_lsb_files(directory_path)
