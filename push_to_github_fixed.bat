@echo off
cd /d %~dp0
git init
git config user.name "mugi-system"
git config user.email "mugi-system@muse.ai"
git add .
git commit -m "Initial commit: MugiLoadImage custom node"
git branch -M main
git remote add origin https://github.com/mugi-system/ComfyUI-MugiLoadImage.git 2>nul
git remote set-url origin https://github.com/mugi-system/ComfyUI-MugiLoadImage.git
git push -u origin main
pause
