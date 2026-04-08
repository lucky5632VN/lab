@echo off
title BASF Virtual Lab - Server
echo ==========================================================
echo       PHONG THI NGHIEM BASF VIRTUAL LAB (OFFLINE)
echo ==========================================================
echo.
echo [*] Dang khoi dong he thong mang ao...
echo [*] Vui long DUNG TAT cua so den nay trong luc choi nhe!
echo.
echo [*] Dang tu dong mo trinh duyet Web...
start http://localhost:8000
echo.

python start_project.py
pause
