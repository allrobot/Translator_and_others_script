# -*- coding:utf-8
import os
import csv
import json
import re

# 用于匹配无法在译文中工作的变量或其它代码
separator_regex='\\\\[a-zA-Z]+\[([^\]]*)\]|\\\\\{|\\\\\||if\([^\)]*\)|\n'

"""
提取译文到字典，返回{原文1:译文1,原文2:译文2...}字典
由于插件只支持{}换行，不支持内部插入\n、\\N[1]、if(\c[1]>0)等参数
只好删掉这些参数，比如原文是：
\\n[1]if(c[0]>0)\\n「　あ、お友達の\\n[3]ちゃんも来たし、今日は学校だからもう　\\c[0]行くね if(v[87]>0)
译文:
\\n[1]if(c[0]>0)\\n「　啊,朋友的\\n[3],而且今天在学校也已经\\c[0]去过if(v[87]>0)
就建立一个对应的字典：
{
"「　あ、お友達の": "「　あ、お友達の":"啊,朋友的",
"ちゃんも来たし、今日は学校だからもう　": "ちゃんも来たし、今日は学校だからもう　":",而且今天在学校也已经",
"行くね": "行くね":"去过"
}

但是，如果AI译文没有原文对应的系统参数，插件输出的译文可能会比较难看
"""
def process_csv_files(directory):
    new_data_dict = {}
    dict_add_symbols={}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r",encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    original_text = row.get("Original Text")
                    initial = row.get("Initial")
                    dict_add_symbols.update({original_text:original_text})
                    if initial is None or initial == "":
                        continue
                    regex_test=re.search(separator_regex,original_text)
                    if regex_test:
                        key_items = re.sub(separator_regex,'\n',original_text).split("\n")
                        key_items[:]=(value for value in key_items if value != "")
                        value_items = re.sub(separator_regex,'\n',initial).split("\n")
                        value_items[:]=(value for value in value_items if value != "")
                        # 译文JSON
                        for i in range(len(key_items)):
                            dict_add_symbols[original_text]=dict_add_symbols[original_text].replace(key_items[i],"{"+key_items[i]+"}")
                            try:
                                new_data_dict[key_items[i]] = value_items[i]
                            except:
                                new_data_dict[key_items[i]]=""

                    else:
                        dict_add_symbols[original_text] = "{" + original_text + "}"
                        new_data_dict[original_text] = initial

    return dict_add_symbols,new_data_dict



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
print(f"\n已保存至\n{output_file_path}\n\n可以移动locales文件夹放至www目录，然后配置多语言翻译插件\n注：DKTools_Localization.js插件")


# 保存T++导入格式CSV
new_dir1=os.path.join(directory_path,"原文添加双{}")
if not os.path.exists(new_dir1):
    os.makedirs(new_dir1)
output_file_path = os.path.join(new_dir1,"T++导入该文件然后覆盖data.csv")
save_dict_as_csv(trans_dict, output_file_path)
print(f"\nT++导入\n{output_file_path}\n然后导出到data覆盖，用于多语言插件要求原文格式，否则插件无法加载原文并且翻译")

