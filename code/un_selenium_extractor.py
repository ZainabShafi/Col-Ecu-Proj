from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

# Set up the download directory
download_dir = '/home/kyle/Desktop/no_git/zainab_human_rights_project/un_selenium_rip_files'

# Configure WebDriver to handle downloads
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True
}
options.add_experimental_option("prefs", prefs)

# Initialize the WebDriver
driver = webdriver.Chrome(options=options)

# Open the target webpage
driver.get("https://unstats.un.org/sdgs/dataportal/countryprofiles/ECU#goal-2")  # Replace with the actual URL


# # Keep the browser open for 100 seconds
# time.sleep(10000)

WebDriverWait(driver, 10).until(
    EC.invisibility_of_element((By.CLASS_NAME, "ReactModal__Overlay"))  # Replace with the actual class of the overlay
)

# # Keep the browser open for 100 seconds
# time.sleep(10000)

# Find all elements with the specified class name
elements = driver.find_elements(By.CLASS_NAME, "StyledIconClass-gqzbmz-0")

# ActionChains instance for coordinate clicks
actions = ActionChains(driver)

# Define coordinates for blank space clicks (example: 100, 200)
blank_space_coords = (0, 0)

for i, element in enumerate(elements):
    try:
        # Click on blank space first for every other click
        if i % 2 == 0:
            actions.move_by_offset(blank_space_coords[0], blank_space_coords[1]).click().perform()
            # time.sleep(1)
            actions.move_by_offset(-blank_space_coords[0], -blank_space_coords[1]).perform()  # Move cursor back

        # Click on the actual element
        element.click()
        # time.sleep(1)  # Optional: wait a second between clicks

    except Exception as e:
        print(f"Could not click on element: {e}")

# # Keep the browser open for 100 seconds
# time.sleep(10000)

# Cleanup: Close the browser
driver.quit()