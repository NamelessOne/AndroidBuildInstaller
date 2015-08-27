call rd output /s /q
call python configParser.py
call timeout /t 5
call cd output
call python googleplayversiongrabber.py
call timeout /t 5
::call ant nodeps clean
::call timeout /t 5
call xcopy ..\dexedLibs bin\dexedLibs\  /s /e
call timeout /t 5
call ant -listener net.sf.antcontrib.perf.AntPerformanceListener nodeps release -l "log.txt"
pause