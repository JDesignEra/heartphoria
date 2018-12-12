@echo off
set FLASK_APP=heartphoria
set FLASK_ENV=development
:loop
set /p command=py -m flask 
if '%command%'=='quit' goto eof
py -m flask %command%
goto loop
