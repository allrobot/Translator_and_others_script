# -*- coding:utf-8
import os
import csv
import json

"""
提取译文到字典，返回{原文:译文}字典
同时也分割
"""
def process_csv_files(directory):
    new_data_dict = {}
    trans_data_dict={}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r",encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    original_text = row.get("Original Text")
                    initial = row.get("Initial")

                    if initial is None or initial == "":
                        continue

                    if '\n' in original_text:
                        key_items = original_text.split("\n")
                        value_items = initial.split("\n")
                        for i in range(len(key_items)):
                            try:
                                new_data_dict[key_items[i]] = value_items[i]
                            except:
                                new_data_dict[key_items[i]]=""
                    else:
                        new_data_dict[original_text] = initial
                    trans_data_dict[original_text] = initial
    return trans_data_dict,new_data_dict

"""
给原文添加{}，\\n换行符前的子字符串添加到{}之间
"""
def process_origin_text_add_symbol(dict):
    new_dict={}
    for key in dict.keys():
        new_dict.update({key:"{"+key.replace('\n','}{')+"}"})
    return new_dict

"""
字典保存成main.json，然后放到locales/zh文件夹就可以了
"""
def save_dict_as_json(data_dict, output_file):
    with open(output_file, "w",encoding='utf-8') as file:
        json.dump(data_dict, file,indent=4,ensure_ascii=False)

"""
添加{}保存成CSV文件
"""
def save_dict_as_csv(data_dict, output_file):
    fieldnames = ['Original Text', 'Initial']

    with open(output_file, 'w', newline='',encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for key, value in data_dict.items():
            writer.writerow({'Original Text': key, 'Initial': value})


# 指定目录路径
while True:
    directory_path = input("\nTranslator++生成的CSV文件（已翻译）转换为DKTools_Localization插件所需译文JSON以及原文{}格式\n请输入指定目录：\n")
    if not os.path.isdir(directory_path):
        print("\n请输入目录，而不是文件！")
        exit(0)
    if not os.path.exists(directory_path):
        local_path = os.path.join(os.path.dirname(os.getcwd()), directory_path)
        if not os.path.exists(local_path):
            print("\n目标路径不存在！")
            exit(0)
        else:
            yes = False
            for filename in os.listdir(directory_path):
                if filename.lower().endswith(".csv"):
                    yes = True
            if not yes:
                print("目标目录没有CSV文件存在！")
                exit(0)
            directory_path=local_path
            break
    else:
        yes=False
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(".csv"):
                yes=True
        if not yes:
            print("目标目录没有CSV文件存在！")
            exit(0)
        break



# 处理CSV文件并生成字典
trans_dict,json_dict= process_csv_files(directory_path)

# 指定输出JSON文件路径
new_dir=os.path.join(directory_path,"locales")
if not os.path.exists(new_dir):
    os.mkdir(new_dir)
output_file_path = os.path.join(new_dir,"main.json")
save_dict_as_json(json_dict, output_file_path) # 将字典保存为JSON文件
print(f"\n已保存至\n{output_file_path}\n\n可以移动locales文件夹放至www目录，然后配置多语言翻译插件\n需DKTools_Localization.js")


# 保存T++导入格式CSV
origin_dict=process_origin_text_add_symbol(trans_dict)
new_dir1=os.path.join(directory_path,"原文添加双{}","ctrl")
if not os.path.exists(new_dir1):
    os.makedirs(new_dir1)
output_file_path = os.path.join(new_dir1,"T++导入该文件然后覆盖data.csv")
save_dict_as_csv(origin_dict, output_file_path)
print(f"\nT++导入\n{output_file_path}\n然后导出到data覆盖，用于多语言插件要求原文格式，否则插件无法加载原文并且翻译")

