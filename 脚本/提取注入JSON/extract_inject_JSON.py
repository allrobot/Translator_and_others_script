# -*- coding:utf-8
import copy
import os,json
import re

import sys

import send2trash

# 检查是否至少有一个命令行参数
print("请输入目标JSON文件名，或选中目标文件按下ctrl+shift+c快捷键快速复制文件路径，黏贴到此处：")
while True:
    file_path = input("\n文件路径：\n")
    dir_name = os.path.dirname(os.getcwd())
    if os.path.exists(file_path):
        break
    else:
        file_path = os.path.join(dir_name, file_path)
        if not os.path.exists(file_path):
            print("\n提取注入JSON文件路径不存在！！！")


dirname = os.path.dirname(file_path)
new_dirname = os.path.join(dirname, '待翻译目录')
if not os.path.exists(new_dirname):
    os.mkdir(new_dirname)
save_file_path = os.path.join(new_dirname, '待翻译.json')
def extract_wait_trans():
    with open(file_path, 'r', encoding='utf-8') as file:
        orign_content = json.load(file)
    new_dict = {}
    for key in orign_content.keys():
        # 译文为空
        if orign_content[key] == "":
            new_dict.update({key: ""})
        # 原文和译文相同，大概率是原文
        if key == orign_content[key]:
            new_dict.update({key: ""})
    with open(save_file_path, 'w', encoding='utf-8') as file:
        json.dump(new_dict, file, ensure_ascii=False, indent=4)
        print(f"\n待翻译.json有{new_dict.__len__()}行")
        print("\n\n已创建待翻译文件，请打开翻译工具选择 待翻译目录 文件夹\nAiNiee翻译设置选择MTool模式然后翻译……")
    print("\n输入yes或no，输入yes 待翻译_translated.json 进行注入到新文件，输入no退出脚本")
    load_path = os.path.join(new_dirname, '待翻译_translated.json')
    while True:
        answer=input("\n请输入")
        if answer=="yes":
            if os.path.exists(load_path):
                inject()
                exit(0)
            else:
                print("\n待翻译_translated.json 不存在！！！")
        elif answer=="no":
            exit(0)
        else:
            print("\n输入非yes或no，麻烦重新输入")

def inject():
    global file_path
    load_path=os.path.join(new_dirname,'待翻译_translated.json')
    # load_path为 待翻译_translated.json
    with open(load_path, 'r', encoding='utf-8') as file:
        translated_content = json.load(file)
    # file_path为 transDic.output.json
    with open(file_path, 'r', encoding='utf-8') as file:
        orign_content = json.load(file)
    new_content=copy.deepcopy(orign_content)
    for key in translated_content.keys():
        new_content[key] = translated_content[key]

    file_path=os.path.join(dirname,'完成翻译了，删掉前缀transDic.json')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(new_content, file, ensure_ascii=False, indent=4)
        print("\n完成翻译，可以用SExtract注入了\n\n文件已保存至",file_path)
        send2trash.send2trash(new_dirname)

if __name__ == '__main__':
    extract_wait_trans()
