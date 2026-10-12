import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Fixture for setting up and tearing down the driver
@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

# Helper to get alert text safely
def get_alert_text(driver):
    alert = WebDriverWait(driver, 5).until(
        EC.alert_is_present()
    )
    text = alert.text
    alert.accept()
    return text


# Test 1: Empty username
def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "email").send_keys("shreya@example.com")
    driver.find_element(By.NAME, "student_id").send_keys("101")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    alert_text = get_alert_text(driver)

    assert alert_text == "Username cannot be empty."

# Test 3: Invalid email
def test_invalid_email(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya")
    driver.find_element(By.NAME, "email").send_keys("shreya@")
    driver.find_element(By.NAME, "student_id").send_keys("101")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # The browser's built-in email validation may block submission
    # before the JavaScript validation function runs.
    email_field = driver.find_element(By.NAME, "email")

    assert email_field.get_attribute("validity") is not None
    assert email_field.get_attribute("type") == "email"


# Test 4: Empty email
def test_empty_email(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya")
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "student_id").send_keys("101")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    alert_text = get_alert_text(driver)

    assert alert_text == "Email cannot be empty."


# Test 5: Empty student ID
def test_empty_student_id(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya")
    driver.find_element(By.NAME, "email").send_keys("shreya@example.com")
    driver.find_element(By.NAME, "student_id").clear()
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    alert_text = get_alert_text(driver)

    assert alert_text == "Student ID cannot be empty."


# Test 6: Valid registration
def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya")
    driver.find_element(By.NAME, "email").send_keys("shreya@example.com")
    driver.find_element(By.NAME, "student_id").send_keys("101")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    # Wait until the success page loads
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "h1"),
            "Registration Successful"
        )
    )

    # Verify URL
    assert "/register" in driver.current_url

    # Verify registration details
    body_text = driver.find_element(By.TAG_NAME, "body").text

    assert "Registration Successful" in body_text
    assert "Welcome, Shreya!" in body_text
    assert "Your email is: shreya@example.com" in body_text
    assert "Your student ID is: 101" in body_text