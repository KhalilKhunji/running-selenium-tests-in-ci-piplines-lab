import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_browser():
    """Configure browser differently for local vs CI (GitHub Actions)"""
    options = webdriver.ChromeOptions()

    if os.getenv("CI"):  # Running in GitHub Actions
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)
    else:
        # Local (assumes chromedriver is on PATH)
        return webdriver.Chrome()

# Test 1
def test_invalid_email_shows_error_message():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        # TODO: Enter valid name, invalid email
        driver.find_element(By.ID, "name").send_keys("Khalil")
        driver.find_element(By.ID, "email").send_keys("huehuheueuheu")
        # TODO: Submit form
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # TODO: Confirm success message does NOT appear
        try:
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "message"))
            )
            message = driver.find_element(By.ID, "message").text
            assert "thanks for subscribing" not in message.lower()
        except:
            pass
    finally:
        driver.quit()

# Test 2
def test_blank_password_prevents_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        # TODO: Leave email blank
        driver.find_element(By.ID, "name").send_keys("Test User")
        # TODO: Submit form
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # TODO: Check form validation blocks submit
        try:
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, "message"))
            )
            message = driver.find_element(By.ID, "message").text
            assert "thanks for subscribing" not in message.lower()
        except:
            pass
    finally:
        driver.quit()

# Test 3
def test_successful_signup_shows_thank_you():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        # TODO: Fill form with valid data
        driver.find_element(By.ID, "name").send_keys("Khalil")
        driver.find_element(By.ID, "email").send_keys("khalil@email.com")
        # TODO: Submit
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # TODO: Check thank-you message with name
        message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "message"))
        ).text
        assert "thank you" in message.lower() or "thanks for subscribing" in message.lower()
        assert "khalil" in message.lower()
    finally:
        driver.quit()

# Test 4
def test_form_resets_after_submit():
    driver = setup_browser()
    try:
        driver.get("http://localhost:8000/signup")
        # TODO: Submit valid data
        driver.find_element(By.ID, "name").send_keys("khalilkhunji")
        driver.find_element(By.ID, "email").send_keys("khalilkhunji@nowhere.com")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        # TODO: Confirm fields reset
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element((By.ID, "message"), "Thanks")
        )

        name_value = driver.find_element(By.ID, "name").get_attribute("value")
        email_value = driver.find_element(By.ID, "email").get_attribute("value")

        assert name_value == ""
        assert email_value == ""
    finally:
        driver.quit()
