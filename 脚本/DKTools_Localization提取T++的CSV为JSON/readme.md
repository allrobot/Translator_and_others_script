https://dk-plugins.ru/mv/system/localization/

DKTools_Localization插件，版本5.3.1

假如要汉化某个生肉日本黄油

## 翻译过程

Translator++汉化的差不多了，导出到WWW/data中覆盖，游戏一切游玩正常无报错
那么把T++导出到CSV，然后复制保存CSV的路径

打开bat，输入刚复制的路径，生成`locales`和`原文添加双{}`文件夹，
即可生成插件所需的原文CSV和插件所需译文JSON或CSV文件

把`locales`文件夹移到www目录下，插件配置选CSV或JSON皆可（CSV分隔符为`,`）

T++导入`原文添加双{}`路径下的csv文件，插件所需的原文必须用大括号包裹，一行文本则一个{}，脚本自动跳过\n、\c[0]、if(\v[1])之类的参数

只有这样DKTools_Localization插件才能加载{xxx部分原文xxxx}然后加载对应的译文
>有些{}译文超出游戏文本框限制了，怎么办？怎么换行？
>先在T++用JS脚本自动换行，然后导出为CSV重复以上步骤操作，请在T++导出为CSV前搞定好！！！

插件的参考链接：https://www.bilibili.com/video/BV1Qv4y1B7dt

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

img/system/flag_xx或locale_xx有时会报错找不到，明明该路径已经存在这些图片

===标题屏幕上的按钮===
按钮图形：删掉这个

===外观===
标志文件名：删掉这个


