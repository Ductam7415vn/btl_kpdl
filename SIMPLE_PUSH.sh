#!/bin/bash
# ONE CLICK PUSH TO GITHUB

cd /Users/ductampro/Desktop/BTL_KPDL
git init
git add .
git commit -m "Complete BTL KPDL Project"
git branch -M main
git remote add origin https://github.com/Ductam7415vn/btl_kpdl.git 2>/dev/null
git push -u origin main --force