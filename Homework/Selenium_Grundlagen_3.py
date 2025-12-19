from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

BASE_URL = "https://automationexercise.com"

def main():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    # E-Mail mit Zeitstempel, damit sie einzigartig ist
    unique_email = f"testuser_{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
    username = "TestUser"

    try:
        # 1) URL öffnen
        driver.get(BASE_URL)

        # 2) Startseite sichtbar?
        # Einfach prüfen, dass ein zentrales Element da ist, z.B. der Slider oder "Home"
        assert "Automation Exercise" in driver.title

        # 3) Auf "Signup / Login" klicken
        signup_login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Signup / Login')]"))
        )
        signup_login_btn.click()

        # 4) "New User Signup!" sichtbar?
        new_user_header = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//h2[text()='New User Signup!']"))
        )
        assert new_user_header.is_displayed()

        # 5) Name & E-Mail eingeben
        name_input = driver.find_element(By.NAME, "name")
        email_input = driver.find_element(By.XPATH, "//input[@data-qa='signup-email']")
        name_input.send_keys(username)
        email_input.send_keys(unique_email)

        # 6) Auf "Signup" klicken
        signup_button = driver.find_element(By.XPATH, "//button[@data-qa='signup-button']")
        signup_button.click()

        # 7) "ENTER ACCOUNT INFORMATION" sichtbar?
        account_info_header = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Enter Account Information']"))
        )
        assert account_info_header.is_displayed()

        # 8) Details ausfüllen: Titel, Name, E-Mail, Passwort, Geburtsdatum
        # Titel (Mr/Mrs)
        driver.find_element(By.ID, "id_gender1").click()  # Mr

        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys("SuperSicher123!")

        # Geburtsdatum (Day, Month, Year)
        Select(driver.find_element(By.ID, "days")).select_by_value("10")
        Select(driver.find_element(By.ID, "months")).select_by_value("5")   # Mai
        Select(driver.find_element(By.ID, "years")).select_by_value("1995")

        # 9) Newsletter & Angebote anhaken
        driver.find_element(By.ID, "newsletter").click()
        driver.find_element(By.ID, "optin").click()

        # 10) Adresse & weitere Daten
        driver.find_element(By.ID, "first_name").send_keys("Max")
        driver.find_element(By.ID, "last_name").send_keys("Mustermann")
        driver.find_element(By.ID, "company").send_keys("Beispiel GmbH")
        driver.find_element(By.ID, "address1").send_keys("Musterstraße 1")
        driver.find_element(By.ID, "address2").send_keys("2. OG")
        Select(driver.find_element(By.ID, "country")).select_by_visible_text("Canada")  # irgendein Land
        driver.find_element(By.ID, "state").send_keys("Ontario")
        driver.find_element(By.ID, "city").send_keys("Toronto")
        driver.find_element(By.ID, "zipcode").send_keys("12345")
        driver.find_element(By.ID, "mobile_number").send_keys("+491234567890")

        # 11) "Create Account" klicken
        driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()

        # 12) "ACCOUNT CREATED!" sichtbar?
        account_created_header = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']"))
        )
        assert account_created_header.is_displayed()

        # 13) "Continue" klicken
        driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

        # Es kann sein, dass ein Popup/Ad-Frame stört. Evtl. kurz warten:
        time.sleep(2)

        # 14) "Logged in as username" sichtbar?
        logged_in_text = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//a[contains(text(),'Logged in as {username}')]")
            )
        )
        assert logged_in_text.is_displayed()

        # 15) "Delete Account" klicken
        delete_account_link = driver.find_element(
            By.XPATH, "//a[contains(text(),'Delete Account')]"
        )
        delete_account_link.click()

        # 16) "ACCOUNT DELETED!" sichtbar?
        account_deleted_header = wait.until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Deleted!']"))
        )
        assert account_deleted_header.is_displayed()

        # 17) Auf "Continue" klicken
        driver.find_element(By.XPATH, "//a[@data-qa='continue-button']").click()

        print("Registrierung & Löschung erfolgreich durchgelaufen.")

        time.sleep(2)  # nur zum Beobachten
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
