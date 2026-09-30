@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3 "01_analisis_ventas\analizar.py"
) else (
    python "01_analisis_ventas\analizar.py"
)
if errorlevel 1 echo Revise LEEME_PRIMERO.md para instalar o configurar Python.
pause
