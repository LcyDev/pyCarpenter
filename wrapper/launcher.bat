@echo off
title Loading Wood Rewritten...

:: Construct path to executable
set "path=%~dp0libraries\Wood.exe"

:: Use start command for visibility and control
start "" "%path%"