@echo off
chcp 65001
setlocal enabledelayedexpansion

REM 获取当前目录
pushd %~dp0

for %%i in (*.*) do (
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
set "outputFile=!inputFile!已压片.mp4"
REM 2k分辨率，-b:v 5M改-b:v 10M码率即可
ffmpeg -vsync 0 -hwaccel cuvid -c:v h264_cuvid -i "!inputFile!" -c:a copy -c:v h264_nvenc -b:v 5M "!outputFile!"
endlocal
pause
