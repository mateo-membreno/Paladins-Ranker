# Paladins-Ranker

## Summary 

The main program flow:

start with 3 queues
1. stores match ids --> for finding player who were in that game
2. stores player profiles --> for finding match ids of games they played
3. stores match ids --> to scrape match data from that game

main program flow
1. thread 1 does a BFS on queue 1 and adds results to queue 2
2. thread 2 does BFS on queue 2 and adds results to queue 1 and 3
3. thread 3 takes from queue 3 and scrapes data from that page


use sets to track for duplicate ids and players


queues are thread safe in python, so only needed to worry about the sets

## Other Details
- Uses Beautiful Soup for webscraping
- SQLite for database
- Tensorflow Keras for classifcation model
