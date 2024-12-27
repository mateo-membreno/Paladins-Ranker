import threading
import queue

import scrape
import database


# Thread-safe queues
unscraped_ids = queue.Queue()
unscraped_profiles = queue.Queue()

# Sets for scraped data
scraped_ids = set()
scraped_profiles = set()

# Lock for thread-safe access to shared sets
id_lock = threading.Lock()
profile_lock = threading.Lock()

def process_match_ids():
    while True:
        if not unscraped_ids.empty():
            id = unscraped_ids.get()
            with id_lock:
                if id in scraped_ids:
                    continue
                scraped_ids.add(id)

            match_data = scrape.scrape_match_data(id)
            profile_links = scrape.get_player_profiles(id)

            # add to links queue
            for profile in profile_links:
                with profile_lock:
                    if profile not in scraped_profiles:
                        unscraped_profiles.put(profile)

            # Store match data in the database
            database.store_match_data(match_data)

def process_profiles():
    while True:
        if not unscraped_profiles.empty():
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


def store_match_data(match_data):
    # Replace with actual database storage logic
    print(f"Storing match data: {match_data}")

#innitialize id list
unscraped_ids.put("1262539296")

# Start threads
match_thread = threading.Thread(target=process_match_ids, daemon=True)
profile_thread = threading.Thread(target=process_profiles, daemon=True)

match_thread.start()
profile_thread.start()

# Keep the main thread alive to allow worker threads to run
match_thread.join()
profile_thread.join()
