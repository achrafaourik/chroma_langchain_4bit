#!/bin/sh

echo "Starting makemigrations"
python3 manage.py flush --no-input
python3 manage.py makemigrations
python3 manage.py collectstatic --no-input
echo "Finished makemigrations"

echo "Starting migrate"
python3 manage.py migrate
echo "Finished migrate"

# python -m spacy download en_core_web_md

# #echo "Starting Rasa Train model"
# rasa train
# #echo "Finised Rasa Train"

# rasa run -m models --enable-api --cors "*" & rasa run actions &
# echo "starting kobold server"
# ./play.sh & echo "started kobold server" &

exec "$@"