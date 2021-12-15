#!/usr/bin/bash

REPO_URL=$(git remote get-url origin)

rm -rf _build/.build
make clean
make html
cd _build
git clone -b gh-pages $REPO_URL .build
cp -r _build/html/* .build/.
cd .build
git add .
git commit -m "publish"
git push origin
cd ../..
