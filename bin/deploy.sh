#!bin/bash
docker-compose up --scale fit_gururecommender=0 --scale predict_gururecommender=0 --scale tweepy_crawler=0 --scale recommend_gururecommender=0 --build