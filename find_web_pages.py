from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

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
start_number = 1220879781
end_number = 1220879783

# List to store the matching numbers
matching_numbers = []

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
    except:
        print(number, "is not a match ID")

# Quit the driver and close the browser
driver.quit()

# Print the list of matching numbers
print("Matching numbers:")
for number in matching_numbers:
    print(number)
