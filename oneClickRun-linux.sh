#!/usr/bin/env sh

sudo apt install default-libmysqlclient-dev

pip install -r ./backend/requirements.txt
cd frontend && npm install
npm run build
cd .. # go back to the project root directory

python3 -m spacy download en_core_web_sm

cd backend
python3 ./app.py