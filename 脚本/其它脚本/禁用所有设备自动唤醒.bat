@echo off
setlocal enabledelayedexpansion

REM 执行 powercfg 命令并将输出保存到临时文件
powercfg /devicequery wake_programmable > tmptmptmp.txt

REM 逐行读取临时文件的内容，并对每行进行处理
for /f "tokens=*" %%a in (tmptmptmp.txt) do (
  set "line=%%a"

  REM 在每行前面添加命令前缀和后缀
  set "line=powercfg /devicedisablewake "!line!""

  REM 执行处理后的命令
  echo !line!
)

REM 删除临时文件
del tmptmptmp.txt

endlocal
pause