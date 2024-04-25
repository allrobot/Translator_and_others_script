可以参考：[Github个人用插件](https://github.com/allrobot/Translator_and_others_script/tree/main/脚本/Localization多语言MV插件的提取注入)

官方插件：https://dk-plugins.ru/mv/system/localization/

DKTools_Localization完全汉化版本插件，Ver 5.3.1，目前最新的插件版本为5.5.7

假如要汉化某个生肉，手动给原文添加{}无疑是一件非常累人的工作，尤其是原文添加{}不能加入参数变量

原文示例：

```text
\n[1]
「　あ、お友達の\n[3]ちゃんも来たし、今日は学校だからもう　行くね
```

原文正确添加{}示例：

```text
\n[1]
「　{あ、お友達の}\n[3]{ちゃんも来たし、今日は学校だからもう　行くね}
```

应该翻译成：

```text
\n[1]
「　啊，我的朋友\n[3]也来了，而且今天是上学的日子，我们走吧。
```

那么`locales/zh/main.json`的内容应该写：

```JSON
{
	"あ、お友達の":"啊，我的朋友",
	"ちゃんも来たし、今日は学校だからもう　行くね":"也来了，而且今天是上学的日子，我们走吧。"
}
```

很显然，这是一个较大的工作量，所以个人写了py脚本，点击bat即可一次性完成原文添加{}，生成翻译.json的工作

 代码：[DKTools_Localization处理原文译文脚本](https://github.com/allrobot/Translator_and_others_script/blob/main/%E8%84%9A%E6%9C%AC/Localization%E5%A4%9A%E8%AF%AD%E8%A8%80MV%E6%8F%92%E4%BB%B6%E7%9A%84%E6%8F%90%E5%8F%96%E6%B3%A8%E5%85%A5/extract_from_csv_transcoding_to_json.py)

前提是译者已完成翻译工作，py脚本通过Translator++提取的csv进行处理，生成带{}的csv和locales/zh/main.json

带{}的csv，需Translator++把新创建的csv文件进行注入，然后覆盖到原文data文件夹

## 翻译过程

Translator++汉化的差不多了，导出到WWW/data中覆盖，游戏一切游玩正常无报错
那么把T++导出到CSV，然后复制保存CSV的路径

打开bat，输入刚复制的路径，生成`locales`和`原文添加双{}`文件夹，
即可生成插件所需的原文CSV和插件所需译文JSON或CSV文件

把`locales`文件夹移到www目录下，插件配置选CSV或JSON皆可（CSV分隔符为`,`）

T++导入`原文添加双{}`路径下的csv文件，插件所需的原文必须用大括号包裹，一行文本则一个{}，脚本自动跳过\n、\c[0]、if(\v[1])之类的参数

只有这样DKTools_Localization插件才能加载{xxx部分原文xxxx}然后加载对应的译文

> 有些{}译文超出游戏文本框限制了，怎么办？怎么换行？
> 先在T++用JS脚本自动换行，然后导出为CSV重复以上步骤操作，请在T++导出为CSV前搞定！！！

5.3.1插件的参考链接：https://www.bilibili.com/video/BV1Qv4y1B7dt

## 插件配置

工程文件，插件管理器点最下面创建插件，基本配置-名称，点名称拉开脚本列表，选择DKTools和DKTools_Localization插件

### 需配置插件3个地方

===语言===
游戏语言：
{"Language":"日本語","Locale":"ja","Primary":"true"}
{"Language":"简体中文","Locale":"zh","Primary":"false"}
===外观===
帮助文本：
{"Locale":"ja","Text":"言語の選択"}
{"Locale":"zh","Text":"选择您的语言"}
===标题菜单===
显示切换语言命令为True，插件提供了三个地方可供创建切换语言按钮：左上角、标题菜单底部、设置界面底部

### 建议删掉图片地址

img/system/flag_xx或locale_xx有时会报错找不到，明明该路径已经存在这些图片（local_%1 or flag_%1）

===标题屏幕上的按钮===
按钮图形：删掉这个

===外观===
标志文件名：删掉这个
