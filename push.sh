#!/bin/bash

cp -rf ./* ../backup
git pull origin main
git add .
git status
echo "Введите название коммита: "
read NAME
git commit -m $NAME
git push origin main
