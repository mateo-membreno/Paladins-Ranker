from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from scrape_page_2 import scrape_match_2
import pandas as pd


# Specify the path to your ChromeDriver executable
chrome_driver_path = r'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\chrome_driver\chromedriver.exe'

# Create options object
chrome_options = Options()

# Set headless option to true
chrome_options.add_argument('--headless')

# Create a new ChromeDriver service
service = Service(chrome_driver_path)
service.start()

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define the range of numbers to search
start_number = 1220000000
end_number = 1230000000

# List to store the matching numbers
matching_numbers = []

# initialize data frame
df = pd.DataFrame(columns=['Match ID', 'Date', 'Game Mode', 'Winners', 'Losers'])

# Iterate through the numbers in the specified range
for number in range(start_number, end_number + 1):
    # Construct the URL for the current number
    url = f'https://paladins.guru/match/{number}'

    # Open the URL in the browser
    driver.get(url)

    # Check if the webpage contains the specified element
    try:
        match_div = driver.find_element(By.CSS_SELECTOR, 'div.match-table.win')
        matching_numbers.append(number)
        print(f"Match found for number: {number}")
        new_row = scrape_match_2(driver, number)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    except:
        print(number, "is not a match ID")

# Quit the driver and close the browser
driver.quit()

# Print the list of matching numbers
print("Matching numbers:")
for number in matching_numbers:
    print(number)
print(df.head())

# save to csv
csv_file_path = fr'C:\Users\SummerlyCow\Desktop\Paladins-Ranker\Data\{start_number}_{end_number}.csv'

# Save the DataFrame as a CSV file
df.to_csv(csv_file_path, index=False)


print("DataFrame saved as CSV successfully.")
