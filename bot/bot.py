from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("window-size=1400,1000")

def open_sign_in_page():
    opts = Options()
    opts.add_argument("--remote-debugging-port=9222")
    opts.add_experimental_option("detach", True)
    opts.add_argument("--user-data-dir=C:/selenium/GoopiChromeProfile")
    opts.add_argument("window-size=1400,1000")

    driver = webdriver.Chrome(options = opts)
    driver.get("https://www.goopi.co/users/sign_in")

def launch_bot(shopline_product_link, customer_info):
    # Attach to existing browser
    opts = Options()
    opts.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=opts)
    driver.get(shopline_product_link)

    p_product_fill(driver, customer_info)

    p_cart_fill(driver)

    # Page: Checkout, fill payment and recipient info, etc.
    p_checkout_fill_customer_info_form(driver, customer_info)
    p_checkout_fill_recipient_form(driver, customer_info)

def p_product_fill(driver, customer_info):
    """
    Page: Products
    """
    # TODO("顏色/Size/QTY，每樣產品不同，會影響DIV")
    xpaht_size = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/select"
    # xpaht_size = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/select"
    xpath_qty = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/input"
    # xpath_qty = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[3]/div[2]/div/input"
    
    prod_size_field = Select(driver.find_element(by=By.XPATH, value=xpaht_size))
    prod_size_field.select_by_visible_text(customer_info['prod_size'])

    prod_qty_field = driver.find_element(by=By.XPATH, value=xpath_qty)
    prod_qty_field.clear()
    prod_qty_field.send_keys(customer_info['prod_qty'])
    
    xpath_buyNow = "//*[@id=\"#btn-variable-buy-now\"]"
    driver.find_element(By.XPATH, xpath_buyNow).click()

def p_cart_fill(driver):
    """
    Page: Cart

    Don't use explicit waiting.
    """
    time.sleep(5)
    xpath_goCheckout = "//*[@id=\"checkout-container\"]/div/div[3]/div[4]/div[2]/section/div[2]/a"
    go_checkout_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath_goCheckout))
    )
    go_checkout_button.click()

def p_checkout_fill_customer_info_form(driver, customer_info):
    """
    Page: Checkout
    """
    xpath_customer_name = "//*[@id=\"order-customer-name\"]"
    xpath_customer_mail = "//*[@id=\"order-customer-email\"]"
    xpath_customer_phone = "//*[@id=\"order-customer-phone\"]"
    xpath_line_id = "//*[@id=\"user-field-598198f2d4e395db79000a21\"]"

    customer_name_field = driver.find_element(by=By.XPATH, value=xpath_customer_name)
    customer_name_field.clear()
    customer_name_field.send_keys(customer_info['name'])

    customer_mail_field = driver.find_element(by=By.XPATH, value=xpath_customer_mail)
    customer_mail_field.clear()
    customer_mail_field.send_keys(customer_info['email'])

    customer_phone_field = driver.find_element(by=By.XPATH, value=xpath_customer_phone)
    customer_phone_field.clear()
    customer_phone_field.send_keys(customer_info['phone'])

    line_id_field = driver.find_element(by=By.XPATH, value=xpath_line_id)
    line_id_field.clear()
    line_id_field.send_keys(customer_info['line_id'])

def p_checkout_fill_recipient_form(driver, customer_info):
    """
    Page: Checkout
    """
    xpath_recipient_name = "//*[@id=\"recipient-name\"]"
    xpath_recipient_phone = "//*[@id=\"recipient-phone\"]"

    recipient_name_field = driver.find_element(by=By.XPATH, value=xpath_recipient_name)
    recipient_name_field.clear()
    recipient_name_field.send_keys(customer_info['name'])
    recipient_phone_field = driver.find_element(by=By.XPATH, value=xpath_recipient_phone)
    recipient_phone_field.clear()
    recipient_phone_field.send_keys(customer_info['phone'])