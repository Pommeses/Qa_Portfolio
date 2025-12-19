import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# ============================================================
#  BASIS-FIXTURES
# ============================================================

@pytest.fixture(scope="session")
def base_url():
    # Seite mit Produkten
    return "https://grocerymate.masterschool.com/store"


def get_base_root(base_url: str) -> str:
    # https://grocerymate.masterschool.com/store -> https://grocerymate.masterschool.com
    return base_url.rsplit("/", 1)[0]


@pytest.fixture(scope="session")
def driver():
    opts = Options()
    opts.add_argument("--headless=new")          # zum Debuggen auskommentieren
    opts.add_argument("--window-size=1920,1080")
    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()


@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)


@pytest.fixture
def logout(driver):
    def _logout():
        driver.delete_all_cookies()
    return _logout


# ============================================================
#  GENERISCHE HELFER
# ============================================================

def get_element_or_none(driver, by, selector):
    els = driver.find_elements(by, selector)
    return els[0] if els else None


# alle Produktnamen in der Liste
PRODUCT_TITLE_ELEMENT = (By.CSS_SELECTOR, "div.card-header p.lead")


def get_all_product_titles(driver):
    return [el.text.strip() for el in driver.find_elements(*PRODUCT_TITLE_ELEMENT)]


def has_product_title(driver, title: str) -> bool:
    return title in get_all_product_titles(driver)


# ============================================================
#  AGE-GATE (Altersverifikation)
# ============================================================

AGE_GATE_MODAL = (By.CSS_SELECTOR, "div.modal-content")
AGE_GATE_INPUT = (By.CSS_SELECTOR, "div.modal-content input[placeholder='DD-MM-YYYY']")
AGE_GATE_CONFIRM = (By.XPATH, "//div[@class='modal-content']//button[normalize-space()='Confirm']")


def is_age_modal_visible(driver) -> bool:
    modal = get_element_or_none(driver, *AGE_GATE_MODAL)
    return modal is not None and modal.is_displayed()


def enter_birthdate_and_confirm(driver, wait, birthdate_str: str):
    inp = wait.until(EC.visibility_of_element_located(AGE_GATE_INPUT))
    inp.clear()
    inp.send_keys(birthdate_str)
    driver.find_element(*AGE_GATE_CONFIRM).click()


def handle_age_gate_if_present(driver, wait, birthdate_str: str = "01-01-1990"):
    """Age-Gate schließen, falls es eingeblendet wird."""
    try:
        modal = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located(AGE_GATE_MODAL)
        )
    except TimeoutException:
        return
    if modal and modal.is_displayed():
        enter_birthdate_and_confirm(driver, wait, birthdate_str)
        WebDriverWait(driver, 5).until(
            EC.invisibility_of_element_located(AGE_GATE_MODAL)
        )


# ============================================================
#  NAVIGATION & SHOPPING-HELFER
# ============================================================

def open_home(driver, base_url, wait):
    """Produktliste öffnen & Age-Gate bestätigen."""
    driver.get(base_url)
    handle_age_gate_if_present(driver, wait)
    # irgendein Produktbild sichtbar
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.card-img-top")))


def open_first_product_detail(driver, base_url, wait):
    """Erstes Produkt aus der Liste öffnen – über Titel (card-header/lead)."""
    open_home(driver, base_url, wait)
    product_title_el = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.card-header p.lead"))
    )
    product_title_el.click()
    handle_age_gate_if_present(driver, wait)
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "section.productDetailContainer")
        )
    )


def click_add_to_cart_by_index(driver, wait, index: int):
    """n-ten 'Add to cart'-Button klicken."""
    btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             f"(//button[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),"
             f" 'add to cart')])[{index}]")
        )
    )
    btn.click()
    time.sleep(0.5)


def open_cart(driver, wait):
    """
    Warenkorb öffnen über das Icon:
    """
    cart_svg = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//svg[@class='headerIcon-size' and @viewBox='0 0 16 16'"
             " and .//path[starts-with(@d,'M0 2.5A.5.5')]]")
        )
    )
    cart_svg.click()
    wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "section.checkout-section")
        )
    )
    time.sleep(0.5)


def get_product_total(driver) -> float:
    """
    <div class="product-total-container">
      <h5>Product Total:</h5>
      <h5>17.50€</h5>
    </div>
    """
    nodes = driver.find_elements(
        By.CSS_SELECTOR,
        "div.product-total-container h5.fw-bold.mb-0"
    )
    assert len(nodes) >= 2, "product-total-container nicht im erwarteten Format."
    txt = nodes[1].text.strip().replace("€", "").replace(",", ".")
    return float(txt)


def get_shipping_cost(driver) -> float:
    """
    <div class="shipment-container">
      <h5 class="fw-bold mb-0">Shipment:</h5>
      <h5 class="fw-bold mb-0">0€</h5>
    </div>
    """
    nodes = driver.find_elements(
        By.CSS_SELECTOR,
        "div.shipment-container h5.fw-bold.mb-0"
    )
    assert len(nodes) >= 2, "shipment-container nicht im erwarteten Format."
    txt = nodes[1].text.strip().replace("€", "").replace(",", ".")
    return float(txt)


# ====== PLUS / MINUS IM CHECKOUT =====================================

CHECKOUT_FIRST_MINUS = (
    By.CSS_SELECTOR,
    "section.checkout-section .checkout-quantity .minus"
)
CHECKOUT_FIRST_PLUS = (
    By.CSS_SELECTOR,
    "section.checkout-section .checkout-quantity .plus"
)
CHECKOUT_FIRST_QTY_INPUT = (
    By.CSS_SELECTOR,
    "section.checkout-section .checkout-quantity .quantity-input"
)


def click_first_minus(driver, wait):
    btn = wait.until(EC.element_to_be_clickable(CHECKOUT_FIRST_MINUS))
    btn.click()
    time.sleep(0.5)


def click_first_plus(driver, wait):
    btn = wait.until(EC.element_to_be_clickable(CHECKOUT_FIRST_PLUS))
    btn.click()
    time.sleep(0.5)


def get_first_quantity(driver) -> int:
    el = get_element_or_none(driver, *CHECKOUT_FIRST_QTY_INPUT)
    return int(el.get_attribute("value")) if el is not None else 0


# ============================================================
#  LOGIN & USER-FIXTURES
# ============================================================

def do_login(driver, wait, base_url, email: str, password: str):
    """
    Login-Flow Login-HTML:

    <div class="auth-wrapper">
      <form class="form">
        <input type="email" class="form-input">
        <input type="password" class="form-input">
        <button type="submit" class="submit-btn">Sign In</button>
        <a class="home-link">Go to Home</a>
      </form>
    """
    base_root = get_base_root(base_url)
    login_url = base_root + "/login"

    driver.get(login_url)

    email_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "form.form input[type='email'].form-input")
        )
    )
    pwd_input = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "form.form input[type='password'].form-input")
        )
    )

    email_input.clear()
    email_input.send_keys(email)
    pwd_input.clear()
    pwd_input.send_keys(password)

    submit_btn = driver.find_element(By.CSS_SELECTOR, "form.form button.submit-btn")
    submit_btn.click()
    time.sleep(1)

    home_link = get_element_or_none(driver, By.CSS_SELECTOR, "a.home-link")
    if home_link:
        home_link.click()

    # von Home aus weiter zum Shop:
    shop_link = get_element_or_none(driver, By.CSS_SELECTOR, "a[href='/store']")
    if shop_link:
        shop_link.click()
    else:
        # Fallback: direkt auf /store
        driver.get(base_url)

    handle_age_gate_if_present(driver, wait)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img.card-img-top")))


@pytest.fixture
def buyer_user(driver, wait, base_url, logout):
    """
    Käufer-User:
      E-Mail:    Testmail@dot.com
      Passwort:  Test123
    Dieser User hat mindestens einen Kauf und eine Bewertung.
    """
    logout()
    do_login(
        driver,
        wait,
        base_url,
        email="Testmail@dot.com",
        password="Test123",
    )
    return "Testmail@dot.com"


@pytest.fixture
def non_buyer_user(driver, wait, base_url, logout):
    """
    Nicht-Käufer-User:
      E-Mail:    Testmail@dot.de
      Passwort:  Test123
    Dieser User hat bisher keinen Kauf.
    """
    logout()
    do_login(
        driver,
        wait,
        base_url,
        email="Testmail@dot.de",
        password="Test123",
    )
    return "Testmail@dot.de"


# ============================================================
#  TC07 / TC08 – Durchschnittsbewertung
# ============================================================

PRODUCT_DETAIL_SECTION = (By.CSS_SELECTOR, "section.productDetailContainer")
PRODUCT_DETAIL_RATING = (By.CSS_SELECTOR, "section.productDetailContainer div.custom_rating")


def test_tc07_rating_not_in_product_list(driver, base_url, wait, logout):
    """
    TC07 – Durchschnittswert wird nur auf der Produktseite angezeigt.
    """
    logout()
    open_home(driver, base_url, wait)
    stars = driver.find_elements(By.CSS_SELECTOR, "span.star")
    assert len(stars) == 0


def test_tc08_rating_on_product_page(driver, base_url, wait, logout):
    """
    TC08 – Durchschnitt wird auf der Produktseite angezeigt.
    """
    logout()
    open_first_product_detail(driver, base_url, wait)
    assert driver.find_elements(*PRODUCT_DETAIL_SECTION)
    rating = driver.find_element(*PRODUCT_DETAIL_RATING)
    stars = rating.find_elements(By.CSS_SELECTOR, "span.star")
    assert len(stars) > 0

# ============================================================
#  TC-AGE-01 … 05 – Altersverifikation (Modal)
# ============================================================

def test_tc_age_01(driver, base_url, wait, logout):
    """
    TC-AGE-01 – Altersprüfung erscheint beim ersten Aufruf.
    """
    logout()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))
    assert is_age_modal_visible(driver)


def test_tc_age_02(driver, base_url, wait, logout):
    """
    TC-AGE-02 – Keine Speicherung über Cookies:
    Nach Cookie-Löschung muss das Modal erneut erscheinen.
    """
    logout()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))
    enter_birthdate_and_confirm(driver, wait, "01-01-1990")

    driver.delete_all_cookies()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))
    assert is_age_modal_visible(driver)


def test_tc_age_03(driver, base_url, wait, logout):
    """
    TC-AGE-03 – Nutzer muss Geburtsdatum eingeben.
    """
    logout()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))

    driver.find_element(*AGE_GATE_CONFIRM).click()
    time.sleep(0.5)
    assert is_age_modal_visible(driver)


def test_tc_age_04(driver, base_url, wait, logout):
    """
    TC-AGE-04 – Minderjähriger wird blockiert.
    """
    logout()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))

    enter_birthdate_and_confirm(driver, wait, "01-01-2010")
    time.sleep(0.5)
    assert is_age_modal_visible(driver), "Minderjähriger sollte weiter blockiert sein."


def test_tc_age_05(driver, base_url, wait, logout):
    """
    TC-AGE-05 – Volljähriger wird durchgelassen.
    """
    logout()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))

    enter_birthdate_and_confirm(driver, wait, "01-01-1990")
    wait.until(EC.invisibility_of_element_located(AGE_GATE_MODAL))


# === NEU: Altersverifikation + Alkoholfilter ==========================

ALCOHOL_PRODUCT_NAME = "Sötma Strawberry & Lime Cider"


def test_tc_age_06_under18_no_alcohol(driver, base_url, wait, logout):
    """
    TC-AGE-06 – Unter 18: Alkoholische Produkte werden NICHT angezeigt.
    """
    logout()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))
    enter_birthdate_and_confirm(driver, wait, "01-01-2010")  # < 18
    wait.until(EC.invisibility_of_element_located(AGE_GATE_MODAL))

    titles = get_all_product_titles(driver)
    assert ALCOHOL_PRODUCT_NAME not in titles


def test_tc_age_07_over18_sees_alcohol(driver, base_url, wait, logout):
    """
    TC-AGE-07 – Über 18: Alkoholische Produkte werden angezeigt.
    """
    logout()
    driver.get(base_url)
    wait.until(EC.visibility_of_element_located(AGE_GATE_MODAL))
    enter_birthdate_and_confirm(driver, wait, "01-01-1990")  # >= 18
    wait.until(EC.invisibility_of_element_located(AGE_GATE_MODAL))

    titles = get_all_product_titles(driver)
    assert ALCOHOL_PRODUCT_NAME in titles


# ============================================================
#  1. PRODUKTBEWERTUNGEN – TC01–TC06
# ============================================================

# <section class="new-review-section"> ... </section>

REVIEW_SECTION = (By.CSS_SELECTOR, "section.new-review-section")
REVIEW_TEXTAREA = (By.CSS_SELECTOR, "section.new-review-section textarea.new-review-form-control")
REVIEW_SEND_BUTTON = (By.CSS_SELECTOR, "section.new-review-section button.new-review-btn-send")
REVIEW_CANCEL_BUTTON = (By.CSS_SELECTOR, "section.new-review-section button.new-review-btn-cancel")
REVIEW_INTERACTIVE_STARS = (By.CSS_SELECTOR, "section.new-review-section div.interactive-rating span.star")
REVIEW_RESTRICTION = (
    By.XPATH,
    "//*[contains(., 'buy this product') or contains(., 'only after purchase') or contains(., 'nur nach Kauf')]"
)


def test_tc01_guest_cannot_review(driver, base_url, wait, logout):
    """
    TC01 – Gastnutzer sieht kein Bewertungsformular.
    """
    logout()
    open_first_product_detail(driver, base_url, wait)
    form_section = get_element_or_none(driver, *REVIEW_SECTION)
    assert form_section is None


def test_tc02_logged_in_without_purchase_blocked(driver, base_url, wait, non_buyer_user):
    """
    TC02 – Eingeloggt, Produkt NICHT gekauft → Bewertung NICHT möglich.
    """
    open_first_product_detail(driver, base_url, wait)

    form_section = get_element_or_none(driver, *REVIEW_SECTION)
    restriction = get_element_or_none(driver, *REVIEW_RESTRICTION)
    send_btn = get_element_or_none(driver, *REVIEW_SEND_BUTTON)

    assert (
        form_section is None
        or restriction is not None
        or (send_btn is not None and not send_btn.is_enabled())
    )


def test_tc03_logged_in_with_purchase_can_review(driver, base_url, wait, buyer_user):
    """
    TC03 – Registrierter Nutzer nach Kauf → Bewertung möglich.
    """

    #Login

    open_first_product_detail(driver, base_url, wait)
    form_section = get_element_or_none(driver, *REVIEW_SECTION)
    assert form_section is not None, "Käufer sollte das Review-Formular sehen."
    textarea = get_element_or_none(driver, *REVIEW_TEXTAREA)
    assert textarea is not None, "Textarea für Bewertung sollte vorhanden sein."


def test_tc04_logged_in_without_purchase_cannot_edit_or_delete(driver, base_url, wait, non_buyer_user):
    """
    TC04 – Nutzer ohne Kauf versucht Bewertung zu ändern/löschen.
    Erwartung: Keine Bearbeitung/Löschung möglich.
    """
    open_first_product_detail(driver, base_url, wait)

    form_section = get_element_or_none(driver, *REVIEW_SECTION)
    send_btn = get_element_or_none(driver, *REVIEW_SEND_BUTTON)

    assert (
        form_section is None
        or (send_btn is not None and not send_btn.is_enabled())
    )


def test_tc05_user_with_purchase_can_edit_review(driver, base_url, wait, buyer_user):
    """
    TC05 – Nutzer nach Kauf ändert Bewertung.
    """
    open_first_product_detail(driver, base_url, wait)

    textarea = wait.until(EC.visibility_of_element_located(REVIEW_TEXTAREA))
    old_text = textarea.get_attribute("value")

    new_text = f"{old_text} - edited by test"
    textarea.clear()
    textarea.send_keys(new_text)
    driver.find_element(*REVIEW_SEND_BUTTON).click()
    time.sleep(1)

    driver.refresh()
    handle_age_gate_if_present(driver, wait)
    wait.until(EC.visibility_of_element_located(REVIEW_TEXTAREA))

    textarea_after = driver.find_element(*REVIEW_TEXTAREA)
    current_text = textarea_after.get_attribute("value")
    assert current_text == new_text, (
        f"Erwartet: '{new_text}' im Review-Feld, gefunden: '{current_text}'"
    )


def test_tc06_user_with_purchase_can_delete_review(driver, base_url, wait, buyer_user):
    """
    TC06 – Nutzer nach Kauf löscht Bewertung.
    """
    open_first_product_detail(driver, base_url, wait)

    # Dropdown / Delete aus deinem HTML: <div class="dropdown-menu"><button>Edit</button><button>Delete</button></div>
    delete_btn = get_element_or_none(
        driver,
        By.XPATH,
        "//div[contains(@class,'dropdown-menu')]//button[normalize-space()='Delete']"
    )
    assert delete_btn is not None, (
        "delete nicht vorhanden"
    )

    delete_btn.click()
    time.sleep(1)

    form_section = get_element_or_none(driver, *REVIEW_SECTION)
    textarea = get_element_or_none(driver, *REVIEW_TEXTAREA)

    assert (
        form_section is None
        or (textarea is not None and (textarea.get_attribute("value") or "").strip() == "")
    )


# ============================================================
#  3. VERSANDKOSTEN – TC-S-01 … TC-S-04
# ============================================================

def test_shipping_base(driver, base_url, wait, logout):
    """
    Basis-Test: Warenkorb öffnen & Product Total / Shipment lesbar.
    """
    logout()
    open_home(driver, base_url, wait)
    click_add_to_cart_by_index(driver, wait, 1)
    open_cart(driver, wait)

    total = get_product_total(driver)
    shipment = get_shipping_cost(driver)
    assert total > 0
    assert shipment >= 0


def test_tc_s_01_exact_20_free_shipping(driver, base_url, wait, logout):
    """
    TC-S-01 – Bestellwert genau 20 € → Versandkosten entfallen.
    """
    logout()
    open_home(driver, base_url, wait)

    # -
    click_add_to_cart_by_index(driver, wait, 1)

    open_cart(driver, wait)
    total = get_product_total(driver)
    shipment = get_shipping_cost(driver)

    assert abs(total - 20.0) < 0.01, f"Product Total ist {total}, sollte 20€ sein."
    assert shipment == 0.0, "Bei genau 20€ sollten keine Versandkosten anfallen."


def test_tc_s_02_under_20_shipping_applies(driver, base_url, wait, logout):
    """
    TC-S-02 – Bestellwert unter 20 € → Versandkosten fallen an.
    """
    logout()
    open_home(driver, base_url, wait)

    click_add_to_cart_by_index(driver, wait, 1)
    open_cart(driver, wait)

    total = get_product_total(driver)
    shipment = get_shipping_cost(driver)

    assert total < 20.0, f"Product Total {total} sollte < 20€ sein (Testdaten/Preise prüfen)."
    assert shipment > 0.0, "Unter 20€ müssen Versandkosten > 0 sein."


def test_tc_s_03_shipping_disappears_when_above_20(driver, base_url, wait, logout):
    """
    TC-S-03 – Versandkosten verschwinden, wenn Nutzer über 20 € kommt.
    """
    logout()
    open_home(driver, base_url, wait)

    click_add_to_cart_by_index(driver, wait, 1)
    open_cart(driver, wait)
    shipment_before = get_shipping_cost(driver)
    assert shipment_before > 0.0, "Unter 20€ sollten Versandkosten > 0 sein."

    driver.back()
    time.sleep(0.5)
    click_add_to_cart_by_index(driver, wait, 2)  # weiteres Produkt hinzufügen
    open_cart(driver, wait)

    total_after = get_product_total(driver)
    shipment_after = get_shipping_cost(driver)

    assert total_after > 20.0, f"Product Total {total_after} sollte > 20€ sein."
    assert shipment_after == 0.0, "Über 20€ sollten Versandkosten entfallen."


def test_tc_s_04_shipping_updates_when_total_drops_below_20(driver, base_url, wait, logout):
    """
    TC-S-04 – BUG-Check:
    Wenn der Warenwert nachträglich wieder unter 20€ fällt,
    müssen die Versandkosten wieder 5€ betragen.

    Aktuelles (fehlerhaftes) Verhalten laut Beobachtung:
      Die Versandkosten bleiben 0€, auch wenn der Total < 20€ ist.

    Dieser Test beschreibt das **erwartete** korrekte Verhalten und
    sollte auf der fehlerhaften Implementierung daher FEHLSCHLAGEN.
    """
    logout()
    open_home(driver, base_url, wait)

    # Einen Artikel in den Warenkorb legen und zum Checkout gehen
    click_add_to_cart_by_index(driver, wait, 1)
    open_cart(driver, wait)

    # Menge im Checkout so lange erhöhen, bis wir sicher >= 20€ sind
    while get_product_total(driver) <= 20.5:
        click_first_plus(driver, wait)

    total_above = get_product_total(driver)
    shipment_above = get_shipping_cost(driver)
    assert total_above >= 20.0
    assert shipment_above == 0.0, "Über 20€ sollten die Versandkosten 0€ sein."

    # Jetzt Menge verringern, bis wir wieder unter 20€ fallen
    while get_product_total(driver) >= 19.5 and get_first_quantity(driver) > 1:
        click_first_minus(driver, wait)

    total_below = get_product_total(driver)
    shipment_below = get_shipping_cost(driver)

    assert total_below < 20.0, "Product Total sollte wieder unter 20€ gefallen sein."
    assert shipment_below == 5.0, (
        "Unter 20€ müssen wieder 5€ Versandkosten berechnet werden. "
        "Bleibt der Wert bei 0€, ist das genau der gesuchte Bug."
    )
