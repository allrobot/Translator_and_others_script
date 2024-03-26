
## livemaker

1. 导出livemaker游戏exe内部的文件
```
mkdir game_files
lmar x game.exe -o game_files
```
2. 转换lsb为txt文件，方便查阅
```
cd game_files
lmlsb dump ゲームメイン.lsb > gamemain.txt
lmlsb dump 00000001.lsb > 00000001.lsb.txt
```
3. lsb转换csv，csv转换lsb
```
lmlsb extractcsv --encoding=utf-8-sig 00000001.lsb 00000001.csv
lmlsb insertcsv --encoding=utf-8-sig 00000001.lsb 00000001.csv
```
4. lsb注入到游戏exe
```
lmpatch stopping.exe 00000001.lsb
```
5. 更改字体或修改选项文本
```cmd
# 修改
:: 该命令是显示这类的文本信息，因为选项往往不会在导出的csv中
lmlsb dump --encoding=utf-8 00000033.lsb --mode xml --output-file 00000033.xml
:: 将其转换成人类可阅读的xml格式，然后找到相应的位置，对着文本所在的LineNo="XXX"，使用以下命令：
lmlsb edit 00000033.lsb XXX
:: 修改字体，参考上一步命令
lmlsb dump --encoding=utf-8 メッセージボックス作成.lsb --mode xml --output-file メッセージボックス作成.xml

```


找到包含要编辑的脚本的 lsb 后，将其解压缩。

`mkdir orig_scripts`
编辑脚本。

```
mkdir translated_scripts
cp orig_scripts/*.lns translated_scripts
<run your favorite text editor on whatever script you want to translate>
```
将新脚本修补回 lsb。

`lmlsb insert 00000001.lsb scripts_dir/<translated_script>.lns 1234`
（其中 1234 是适当的 TextIns 命令行号）。
```
$ lmlsb edit メッセージボックス作成.lsb 36
36: MesNew "メッセージボックス" "メッセージボックス土台" 10 10 GetProp("メッセージボックス土台", 5) - 10 - 10 GetProp("メッセージボックス土台", 6) - 10 - 10
1100   "ＭＳ ゴシック" 16 6 16777215 16711680 0 16776960 1  0 "ノベルシステム\メッセージボックス\再生中.lsc" "ノベルシステム\メッセージボックス\イベント.lsc"
    "ノベルシステム\メッセージボックス\右クリック時.lsc"    "ノベルシステム\メッセージボックス\終了.lsc" "ノベルシステム\メッセージボックス\リンク.lsc" 1 4 0
  "ノベルシステム\メッセージボックス\再生開始.lsc"  "ノベルシステム\メッセージボックス\アイドル時.lsc"     0 0 0    0    1 0

Enter new value for each field (or keep existing value)
Name ["メッセージボックス"]: <skipping uneditable field>
PR_PARENT ["メッセージボックス土台"]: <skipping uneditable field>
PR_LEFT [10]:
PR_TOP [10]:
PR_WIDTH [GetProp("メッセージボックス土台", 5) - 10 - 10]: <skipping uneditable field>
PR_HEIGHT [GetProp("メッセージボックス土台", 6) - 10 - 10]: <skipping uneditable field>
PR_ALPHA []: <skipping uneditable field>
PR_PRIORITY [1100]:
...
PR_TAG []: <skipping uneditable field>
PR_CAPTURELINK [1]:
PR_FONTCHANGEABLED [1]: 0
PR_PADDINGLEFT []: <skipping uneditable field>
PR_PADDING_RIGHT []: <skipping uneditable field>
Backing up original LSB.
Wrote new LSB.
```