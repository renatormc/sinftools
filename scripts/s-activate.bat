@echo off
set "VIRTUAL_ENV=%SINFTOOLS%\extras\Python"

if not defined PROMPT (
    set "PROMPT=$P$G"
)

if defined _OLD_VIRTUAL_PROMPT (
    set "PROMPT=%_OLD_VIRTUAL_PROMPT%"
)

if defined _OLD_VIRTUAL_PYTHONHOME (
    set "PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%"
)

set "_OLD_VIRTUAL_PROMPT=%PROMPT%"
set "PROMPT=(sinftools) %PROMPT%"

if defined PYTHONHOME (
    set "_OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%"
    set PYTHONHOME=
)

if defined _OLD_VIRTUAL_PATH (
    set "PATH=%_OLD_VIRTUAL_PATH%"
) else (
    set "_OLD_VIRTUAL_PATH=%PATH%"
)

if defined PYTHONPATH (
    set "_OLD_VIRTUAL_PYTHONPATH=%PYTHONPATH%"
)

set "PYTHONPATH=%SINFTOOLS%\tools\libs"
set "PATH=%VIRTUAL_ENV%;%VIRTUAL_ENV%\Scripts;%PATH%"

:END
