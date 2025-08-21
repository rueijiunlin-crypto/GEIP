# 第一次使用
```bash
git init
git add .
git commit -m "第一次提交"
git remote add origin https://github.com/rueijiunlin-crypto/GEIP
git branch -M main
git push -u origin main
git push -u origin main --force

#後續更新
git add .
git commit -m "整合圖片"
git push

放棄目前本地合併進度（會保留你修改過但未提交的檔案）
git merge --abort

丟掉本地修改、直接覆蓋成遠端版本（⚠會失去本地未提交的更動）
git reset --hard HEAD
git pull
```

# 測試指令:
```bash
py -m http.sever 8000
```


# 連結

https://rueijiunlin-crypto.github.io/GEIP/
