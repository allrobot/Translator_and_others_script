import re
import pyperclip

# 获取剪切板文本内容
clipboard_string=pyperclip.paste()
# 删掉一串英文的首个英文，转换.+
clipboard_string=re.sub('(\s+|)(?:[^a-zA-Z/\r\n]|^)(\s+|)[a-zA-Z]|(?<=^/)[A-Za-z]','.+',clipboard_string)

clipboard_string=re.sub(r'([\s\S]+)',r'/\1/',clipboard_string)

# output
print(clipboard_string)