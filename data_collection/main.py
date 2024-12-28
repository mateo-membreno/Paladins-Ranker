import threading
import queue
import time
import sys

import scrape
import database

run_flag = True
START_MATCH_ID = str(sys.argv[2])
DB_PATH = str(sys.argv[1])

# python queues are already thread safe
unscraped_ids = queue.Queue()
unscraped_profiles = queue.Queue()
unscraped_pages = queue.Queue()

# already seen pfps and ids
scraped_ids = set()
scraped_profiles = set()

id_lock = threading.Lock()
profile_lock = threading.Lock()

def process_match_ids():
    while len(scraped_ids) < 1000:
        if not unscraped_ids.empty():
            try:
                id = unscraped_ids.get()
                unscraped_pages.put(id)
                with id_lock:
                    if id in scraped_ids:
                        continue
                    scraped_ids.add(id)

                profile_links = scrape.get_player_profiles(id)

                # add to links queue
                for profile in profile_links:
                    with profile_lock:
                        if profile not in scraped_profiles:
                            unscraped_profiles.put(profile)
                print(id)
            except Exception as e:
                print(f"Couldn't process id {id}: {e}")
        else:
            time.sleep(0.1)


def process_profiles():
    while run_flag:
        if not unscraped_profiles.empty():
            try:
                profile = unscraped_profiles.get()
                with profile_lock:
                    if profile in scraped_profiles:
                        continue
                    scraped_profiles.add(profile)

                # Simulate getting match IDs for a profile
                match_ids = scrape.get_user_match_ids(profile)

                # Add match IDs to the ID queue
                for id in match_ids:
                    with id_lock:
                        if id not in scraped_ids:
                            unscraped_ids.put(id)
                print(profile)
            except Exception as e:
                print(f"Couldn't process profile {profile}: {e}")
        else:
            time.sleep(0.1)


def process_match_page():
    while run_flag:
        if not unscraped_pages.empty():
            try:
                id = unscraped_pages.get()
                match_data = scrape.scrape_match_data(id)
                database.store_match_data(DB_PATH, match_data)
                print(f"Uploaded match id {id} to db")
            except Exception as e:
                print(f"Error scraping match data for {id}: {e}")
        else:
            time.sleep(0.1)

#innitialize id list
unscraped_ids.put(START_MATCH_ID)

# Start threads
match_thread = threading.Thread(target=process_match_ids, daemon=True)
profile_thread = threading.Thread(target=process_profiles, daemon=True)
page_thread = threading.Thread(target=process_match_page, daemon=True)

threads = [match_thread, profile_thread, page_thread]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()