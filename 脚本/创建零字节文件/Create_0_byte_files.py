# -*- coding:utf-8
import os

while True:
    file_path=input("\n请输入audio文件夹：\n文件路径：\n")
    if os.path.exists(file_path):
        print("\n开始创建零字节文件中……\n")
        break
    else:
        print("\n文件路径不存在！")
test=[]
for root,dirs,files in os.walk(file_path):
    for file in files:
        test.append(os.path.join(root,file))

new_audio_dir=file_path+'零字节，请删掉中文'
if not os.path.exists(new_audio_dir):
    os.mkdir(new_audio_dir)
for file_name in test:
    new_file_path=file_name.replace(file_path,new_audio_dir)
    new_dir=os.path.dirname(new_file_path)
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    print(new_file_path)
    with open(new_file_path,'w') as file:
        continue

print("\n已完成创建零字节的文件们")