https://dk-plugins.ru/mv/system/localization/

DKTools_Localization插件，版本5.3.1

假如要汉化某个生肉日本黄油

插件配置：
工程文件，插件管理器点最下面创建插件，基本配置-名称，点名称拉开脚本列表，选择DKTools和DKTools_Localization插件

### 需配置插件3个地方：

===语言===
游戏语言：
{"Language":"日本語","Locale":"ja","Primary":"true"}
{"Language":"简体中文","Locale":"zh","Primary":"false"}
===外观===
帮助文本：
{"Locale":"ja","Text":"言語の選択"}
{"Locale":"zh","Text":"选择您的语言"}
===标题菜单===
显示命令为True

### 建议删掉：

===标题屏幕上的按钮===
按钮图形：删掉这个

===外观===
标志文件名：删掉这个

img/system/flag_xx或locale_xx有时会报错找不到，明明该路径已经存在这些图片

## 翻译过程

Translator++汉化的差不多了，导出到data，游戏一切游玩正常
那么把T++导出到CSV，然后复制保存CSV的路径

打开bat，输入刚复制的路径，生成`locales`和`原文添加双{}`文件夹

把`locales`文件夹移到www目录下

T++导入`原文添加双{}`路径下的csv文件，里面是一些{}概况起来的，一行文本则一个{}，每个{}都起到换行作用

只有这样，版本5.3.1的插件才能加载{}然后加载对应的译文
>有些{}译文超出游戏文本框限制了，怎么办？怎么换行？
>请在T++导出为CSV前搞定换行！！！

参考链接：https://www.bilibili.com/video/BV1Qv4y1B7dt