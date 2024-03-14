from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException  # updated to include timeoutexception
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime

# Constants
EMAIL = "YOUR_EMAIL"

# function to log messages
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{timestamp} - {message}")

# function to click on the english option
def click_english_option(driver):
    try:
        english_option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'English')]"))
        )
        english_option.click()
        log_message("Selected English from the dropdown.")
    except TimeoutException as e:
        log_message(f"Error selecting English option: {e}")

# function to find and click the decline button
def find_decline_button(driver):
    try:
        decline_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'l17p5q9z') and contains(text(), 'I decline')]"))
        )
        decline_button.click()
        log_message("Decline button clicked.")
        return True
    except TimeoutException as e:
        log_message("Decline button not found within 3 seconds.")
        return False

# function to click the login button
def click_login_button(driver):
    try:
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Log in')]"))
        )
        login_button.click()
        log_message("Login button clicked.")
    except TimeoutException as e:
        log_message(f"Error clicking login button: {e}")

# function to click the login button as a backup
def click_login_button_2(driver):
    try:
        login_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in')]/ancestor::a"))
        )
        login_button.click()
        log_message("Backup login button clicked.")
    except TimeoutException as e:
        log_message(f"Error clicking backup login button: {e}")

# initialize chrome webdriver options
chrome_options = Options()

# initialize the chrome webdriver service
service = Service(ChromeDriverManager().install())

# initialize the chrome webdriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)
log_message("WebDriver initialized.")

# navigate to tinder's login page
driver.get("https://tinder.com/")
log_message("Navigated to Tinder's login page.")

# attempt to click on the decline button and then the primary login button
if find_decline_button(driver):
    click_login_button(driver)
    # try the backup login method if the primary fails or as an additional step
    click_login_button_2(driver)

# click on the english option
click_english_option(driver)

# attempt to find and click the google login button using webdriverwait for consistency
try:
    continue_with_google_spanish = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'nsm7Bb-HzV7m-LgbsSe-BPrWId') and contains(text(), 'Continuar con Google')]"))
    )
    continue_with_google_spanish.click()
    log_message("Clicked on 'Continuar con Google' button successfully.")
except TimeoutException:
    log_message("'Continuar con Google' button not found, attempting in English.")
    try:
        login_with_google_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Continue with Google')]"))
        )
        login_with_google_button.click()
        log_message("Clicked on 'Continue with Google' button successfully.")
    except TimeoutException as e:
        log_message(f"An error occurred: {e}")

# wait for user input to exit
input("Press Enter to exit...\n")

# close the browser
# driver.quit()
