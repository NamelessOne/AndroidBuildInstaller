call rd output /s /q
call python configParser.py
call timeout /t 5
call cd output
call python googleplayversiongrabber.py
call timeout /t 5
call ant clean
call timeout /t 5
call ant debug -l "log.txt"
pause