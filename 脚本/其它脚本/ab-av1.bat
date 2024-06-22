@echo off

:: 定义视频文件扩展名列表
set "video_extensions=mp4,mkv,webm,avi,mov,flv,wmv,mpg,mpeg,3gp,ogv,divx,m4v,rmvb"

:: 遍历所有视频文件扩展名
for %%e in (%video_extensions%) do (
    :: 使用 dir 命令查找所有匹配的视频文件
    for /r %%f in (*.%%e) do (
        :: 调用 ab-av1 命令进行编码
        echo Encoding %%f...
        ab-av1 auto-encode -i "%%f" --preset 4 --svt tune=0 --svt film-grain=4 --svt film-grain-denoise=0 --pix-format yuv420p10le --min-vmaf 93 --max-crf 60 --min-crf 18
    )
)

echo All videos have been encoded.
pause
REM 将ab-av1.bat和ab-av1.exe放在ffmpeg 7.0/bin目录下，在任意视频文件夹下shift+右键打开cmd，输入ab-av1.bat将其启用转换
