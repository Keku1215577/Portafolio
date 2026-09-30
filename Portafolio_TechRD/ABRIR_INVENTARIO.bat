@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
    py -3 "02_gestor_inventario\app.py"
) else (
    python "02_gestor_inventario\app.py"
)
if errorlevel 1 echo Revise LEEME_PRIMERO.md para instalar o configurar Python.
pause
