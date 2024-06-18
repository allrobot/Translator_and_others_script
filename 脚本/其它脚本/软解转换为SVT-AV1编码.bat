@echo off
chcp 65001
setlocal enabledelayedexpansion

REM 获取当前目录
pushd %~dp0

for /r %%i in (*.*) do (
  set ext=%%~xi
  if "!ext!" EQU ".mp4" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".avi" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".mkv" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".mov" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".flv" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".wmv" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".mpeg" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".mpg" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".3gp" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".3g2" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".vob" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".m4v" (
    call :convert_video "%%i"
  ) else if "!ext!" EQU ".m4a" (
    call :convert_video "%%i"
  )
)

goto :eof

:convert_video
setlocal enabledelayedexpansion
set "inputFile=%~1"
set "outputFile=!inputFile!_svt-av1.mkv"

ffmpeg -vsync 0 -hwaccel auto -c:v h264_cuvid -i "!inputFile!" -c:a copy -c:v libsvtav1 -preset 4 -crf 50 -pix_fmt yuv420p10le -svtav1-params tune=2:lp=12:film-grain=4:enable-variance-boost=1 "!outputFile!"
endlocal

rem ffmpeg下载这位构建的版本：https://github.com/BtbN/FFmpeg-Builds/releases
rem 
rem 各类视频压制工具，如格式工厂等，实则是在ffmpeg这一核心工具的基础上，封装了一层图形用户界面（GUI），以简化操作流程，使非专业用户也能轻松上手。
rem 
rem 将ffmpeg的bin目录纳入系统环境变量，我偏好采用软件解码，理由在于，尽管硬件解码（GPU）在处理速度上有优势，但其编码后的文件体积往往较大。相比之下，CPU软解能够生成更为紧凑的视频文件。
rem 
rem 在Windows系统中，可通过快捷键Win+R或Win+Q调出命令提示符窗口，使用cd "路径"指令切换至目标目录。此外，亦可在任意文件夹下，通过Shift+右键点击，于弹出菜单中选择“在此处打开命令窗口”。
rem 
rem 以下为我个人常用的AV1编码配置示例：
rem 
rem 对于2D/3D动画视频：
rem [code]ffmpeg -i input.mp4 -c:a copy -c:v libsvtav1 -preset 4 -crf 50 -pix_fmt yuv420p10le -svtav1-params tune=2:lp=12:film-grain=4:enable-variance-boost=1 output.mkv[/code]
rem 
rem 处理真人视频（例如电视剧、电影）：
rem [code]ffmpeg -i input.mp4 -c:a copy -c:v libsvtav1 -preset 4 -crf 35 -pix_fmt yuv420p10le -svtav1-params tune=2:lp=12:film-grain=8:enable-variance-boost=1 output.mkv[/code]
rem 
rem 输出文件格式可选mp4、mkv或webm等，它们仅作为封装视频数据、字幕、帧信息等的容器。其中，mp4最为普及，mkv因开源特性而支持多种媒体播放，webm则专为网络播放设计。
rem 
rem -c:v libsvtav1 指令调用了svt-av1编码器
rem 
rem -preset 4在平衡视频质量和编码速度方面表现良好。若追求极致画质，可将-preset设为0，但需牺牲大量编码时间，600MB，90秒的视频，H264编码，3840p（4k）分辨率，硬是重编码了13小时……文件体积和使用-preset 4相差不大，都是30MB左右
rem 
rem -crf参数，数值越小意味着更高的画质与更大的文件体积；一般而言，2D/3D动画推荐设定在45~63之间，真人视频则以35为宜。（可以不用加-crf，因为svt-av1默认 -crf 35）
rem 
rem -pix_fmt yuv420p10le （色彩可选0：yuv400、1：yuv420、2：yuv422、3：yuv444） 进一步优化了色彩空间，有助于缩小文件体积，而-svtav1-params则允许对svt-av1编码器进行个性化调整
rem 
rem tune=2 （0 = VQ， 1 = PSNR， 2 = SSIM）选用SSIM算法，即使在-crf较高时，仍能保持较好的视觉效果，不使用tune参数，svt-av1将默认使用PSNR，如果-crf 63，压片后的视频会糊成一团，视觉质量非常糟糕
rem 
rem film-grain=4（0~50）参数则根据视频类型及期望的颗粒感进行调整，具体原理参见文档
rem 
rem lp=12 （取决于电脑芯片的核心数量）win右键选择设备管理器，点处理器，有几个处理器就表示你有几个核心数量，我是i5-12600K，有16个核心数量，设12是ffmpeg防止占用16个核心导致电脑卡顿，同时加快一些编码速度
rem 
rem enable-variance-boost=1（0，默认关闭，1开启） 启用方差增强功能，提升视频细节表现力，它默认variance-boost-strength值为2（1~4），1~4的选项效果咋样参考该文档提供的对
rem 
rem 以上参数的具体含义与应用，可参考官方文档进行深入学习。
