@echo off
cd /d %~dp0
git config user.name "mugi-system"
git config user.email "mugi-system@muse.ai"
git init
git add .
git commit -m "Initial commit: MugiLoadImage custom node"
git branch -M main
git remote add origin https://github.com/mugi-system/ComfyUI-MugiLoadImage.git
git push -u origin main
pause
