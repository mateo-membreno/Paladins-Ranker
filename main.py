from functions import establish_db_connection, scrape_page, insert_data_to_db

# Establish the database connection
db_conn = establish_db_connection()

# Loop over the pages and scrape data
for page in range(1, 101):
    page_url = f"https://example.com/page={page}"
    scraped_data = scrape_page(page_url)

    # Insert the scraped data into the database
    insert_data_to_db(db_conn, scraped_data)

# Close the database connection
db_conn.close()
