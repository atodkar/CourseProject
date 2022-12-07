pip install -r ./backend/requirements.txt
cd frontend
npm install
npm run build
cd .. # go back to the project root directory

python -m spacy download en_core_web_sm

cd backend
python ./app.py