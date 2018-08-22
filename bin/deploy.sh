#!bin/bash
docker-compose up --scale fit_gururecommender=0 --scale predict_gururecommender=0 --build