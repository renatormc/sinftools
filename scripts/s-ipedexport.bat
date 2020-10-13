@echo off
SET PATH=%PATH%;%SINFTOOLS%\extras\iped\iped-3.17-snapshot\tools\tsk\x64
java -jar "%SINFTOOLS%\tools\iped_export\ipedexport-1.0-SNAPSHOT.jar" %*