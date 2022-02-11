@echo off
pyinstaller -w -F --icon=tag_generator.ico tag_generator.py 
copy .\dist\tag_generator.exe .\