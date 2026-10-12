import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


def get_alert_text(driver):
    alert = WebDriverWait(driver, 5).until(
        EC.alert_is_present()
    )
    message = alert.text
    alert.accept()
    return message


def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "email").send_keys("shreya@example.com")
    driver.find_element(By.NAME, "student_id").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    assert get_alert_text(driver) == "Username cannot be empty."


def test_invalid_email(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya")
    driver.find_element(By.NAME, "email").send_keys("invalid-email")
    driver.find_element(By.NAME, "student_id").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    assert get_alert_text(driver) == "Please enter a valid email address."


def test_empty_email(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya")
    driver.find_element(By.NAME, "email").clear()
    driver.find_element(By.NAME, "student_id").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    assert get_alert_text(driver) == "Email cannot be empty."


def test_empty_student_id(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya")
    driver.find_element(By.NAME, "email").send_keys("shreya@example.com")
    driver.find_element(By.NAME, "student_id").clear()
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    assert get_alert_text(driver) == "Student ID cannot be empty."


def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5003/")

    driver.find_element(By.NAME, "name").send_keys("Shreya123")
    driver.find_element(By.NAME, "email").send_keys("shreya@example.com")
    driver.find_element(By.NAME, "student_id").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()

    WebDriverWait(driver, 5).until(
        EC.title_contains("Registration Successful")
    )

    assert "Registration Successful" in driver.page_source
    assert "Shreya123" in driver.page_source
    assert "shreya@example.com" in driver.page_source
    assert "12345" in driver.page_source