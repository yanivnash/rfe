@echo off
setlocal
:PROMPT
SET /P AREYOUSURE=Would you like to install the modules (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END


pip install Pillow
pip install pyperclip
pip install wxPython
pip install paramiko
pip install imageio
pip install imageio-ffmpeg
pip install psutil
pip install pywin32
pip install termcolor
pip install requests
pause