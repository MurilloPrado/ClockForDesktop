@echo off
echo ================================
echo Cleaning old build files...
echo ================================

IF EXIST build rmdir /s /q build
IF EXIST dist rmdir /s /q dist
IF EXIST *.spec del /f /q *.spec

echo ================================
echo Building executable...
echo ================================

python -m PyInstaller --noconfirm --onefile --windowed --add-data "icons;icons" ^ clock.py

echo ================================
echo Copying config...
echo ================================

mkdir dist\config
copy config\settings.json dist\config\settings.json

echo ================================
echo Build finished successfully
echo ================================

pause