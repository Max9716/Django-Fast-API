#!/bin/bash

USER=root              # твой логин на сервере
HOST=45.139.77.206         # IP сервера
REMOTE_DIR=/home/ubuntu/sait   # путь к проекту на сервере
VENV_DIR=$REMOTE_DIR/venv       # путь к venv на сервере
SERVICE=gunicorn               # название сервиса (посмотри через systemctl)


echo ">>> Копирую проект на сервер..."
rsync -avz --delete \
  --exclude 'venv' \
  --exclude '.git' \
  --exclude '__pycache__' \
  ./ $USER@$HOST:$REMOTE_DIR

# ==== ПЕРЕЗАПУСК ====
echo ">>> Перезапускаю Gunicorn..."
ssh $USER@$HOST "cd $REMOTE_DIR && source $VENV_DIR/bin/activate && pip install -r requirements.txt && sudo systemctl restart $SERVICE"

echo ">>> Деплой завершён ✅"