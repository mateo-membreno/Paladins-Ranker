# Paladins-Ranker
***Developement still in progress***

## Summary 

Webscraped match data from top 100 Paladins players to determine opitmal champion pick given teammate and opponent picks

Here is a summary of what this program does:

- The program scrapes match data from Paladins player profiles on paladins.guru. It first collects match IDs by scraping a player's match history pages (find_match_ids_by_player).
- For each match ID, it visits the match page and scrapes key details like date, game mode, map, scores, bans, and player/champion info (scrape_page).
- The scraped data is structured into match data, player data, and damage breakdown data.
- This data is inserted into a MySQL database with functions for establishing a connection, executing inserts, and closing the connection (functions_updating.py).
- The program tracks match IDs already scraped in a JSON file to avoid duplicates.
- Some analysis functions are defined to query the database, like getting win percentage for a champion or finding optimal champion pairings (functions_query.py).

The main program flow:

- Update JSON with new IDs
- Read match IDs from JSON
- Scrape each match page
- Insert data into database

## Other Details
- Uses Selenium and ChromeDriver for web scraping dynamically loaded content
- MySQL and MySQLConnector for database
- JSON for persistent lightweight storage
