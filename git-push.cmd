@REM Begin all REM lines with '@' in case MAVEN_BATCH_ECHO is 'on'
@REM  %~dp0 获取到当前正在执行的脚本的文件夹路径
@echo on

@REM 使用管理员执行的时候，会跳到  C:\Windows\System32 目录下执行该脚本，则加上下面的代码进行目录切换
cd /d %~dp0

@REM set PATH=%PATH%;C:\workspace\coding-install\env-install\Git\cmd

set msg=%1
set commit=%msg%

IF "%msg%"=="" (
    set commit="push github"
)

@REM call git pull

git pull

git add ./
git commit -m %commit%
git push


timeout /t 5 /nobreak >nul
@REM pause
