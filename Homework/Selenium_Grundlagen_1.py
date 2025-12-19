from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def test_count_word_matches_invalid_inputs():
    # Aufgabe 1 (Web-Automatisierung mit Selenium)
    # Testdaten (User Credentials)
    user_name = "standard_user"
    user_password = "secret_sauce"

    # Browser öffnen
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")

    # Eingabefelder und Login-Button finden
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")

    # ausführen
    username_field.send_keys(user_name)
    password_field.send_keys(user_password)
    login_button.click()

    # Warten, um den erfolgreichen Login und die Produktseite zu sehen
    time.sleep(3)

    # Prüfen, ob Login erfolgreich ist
    title_element = driver.find_element(By.CLASS_NAME, "title")
    assert title_element.text == "Products"

    # Prüfen, ob das Produkt "Sauce Labs Backpack" angezeigt wird
    product = driver.find_element(By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
    assert product.text == "Sauce Labs Backpack"

    # Beendet die session
    driver.quit()
