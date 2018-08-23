#!bin/bash
curl -X PUT "localhost:9200/tweets-gurus/_settings" -H 'Content-Type: application/json' -d'{"index" : {"max_result_window" : 1000000}}'
curl -X PUT "localhost:9200/tweets-keywords/_settings" -H 'Content-Type: application/json' -d'{"index" : {"max_result_window" : 1000000}}'
docker-compose run fit_gururecommender