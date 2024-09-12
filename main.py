from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Keep it open
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("window-size=1400,1000")

shopline_product_link = "https://www.goopi.co/products/%E2%80%9Crve-s3%E2%80%9D-riverside-track-shorts-pure-black"

# Page: Products

driver = webdriver.Chrome(options = chrome_options)
# driver.manage().window().maximize()
driver.get(shopline_product_link)

xpath_buyNow = "//*[@id=\"#btn-variable-buy-now\"]"
driver.find_element(By.XPATH, xpath_buyNow).click()


# Page: Cart
# Don't use explicit waiting.
time.sleep(5)
xpath_goCheckout = "//*[@id=\"checkout-container\"]/div/div[3]/div[5]/div[2]/section/div[2]/a"

# wait = WebDriverWait(driver, timeout=5)
# wait.until(lambda d : go_checkout_button.is_displayed())
# go_checkout_button.click()

go_checkout_button = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, xpath_goCheckout))
)
go_checkout_button.click()


# Page: Checkout

## Basic info
customer_name = "蔡英文"
customer_mail = "example@example.com"
customer_phone = "0800092000"
customer_line_id = "777"

## Right: Agreements checkbox
xpath_agree = "//*[@id=\"checkout-container\"]/div/div[5]/div[1]/form/div[1]/label/input"
xpath_submit = "//*[@id=\"place-order-recaptcha\"]"


def fill_customer_info_form():
    xpath_customer_name = "//*[@id=\"order-customer-name\"]"
    xpath_customer_mail = "//*[@id=\"order-customer-email\"]"
    xpath_customer_phone = "//*[@id=\"order-customer-phone\"]"
    xpath_line_id = "//*[@id=\"user-field-598198f2d4e395db79000a21\"]"

    customer_name_field = driver.find_element(by=By.XPATH, value=xpath_customer_name)
    customer_name_field.clear()
    customer_name_field.send_keys(customer_name)

    customer_mail_field = driver.find_element(by=By.XPATH, value=xpath_customer_mail)
    customer_mail_field.clear()
    customer_mail_field.send_keys(customer_mail)

    customer_phone_field = driver.find_element(by=By.XPATH, value=xpath_customer_phone)
    customer_phone_field.clear()
    customer_phone_field.send_keys(customer_phone)

    line_id_field = driver.find_element(by=By.XPATH, value=xpath_line_id)
    line_id_field.clear()
    line_id_field.send_keys(customer_line_id)

fill_customer_info_form()

def fill_recipient_form():
    xpath_recipient_name = "//*[@id=\"recipient-name\"]"
    xpath_recipient_phone = "//*[@id=\"recipient-phone\"]"

    recipient_name_field = driver.find_element(by=By.XPATH, value=xpath_recipient_name)
    recipient_name_field.clear()
    recipient_name_field.send_keys(customer_name)

    recipient_phone_field = driver.find_element(by=By.XPATH, value=xpath_recipient_phone)
    recipient_phone_field.clear()
    recipient_phone_field.send_keys(customer_phone)

fill_recipient_form()

def fill_payment_form():
    xpath_payment_form = "//*[@id=\"checkout-shopline-payment-v2-form\"]/div/div/div[1]/div[2]/div/div/div[1]/div[2]/div/div[1]/div[1]/div"
    iframe = driver.find_elements(By.XPATH, xpath_payment_form)[0]
    driver.switch_to.frame(iframe)

    xpath_field = "//*[@id=\"input-file\"]"
    payment_field = driver.find_element(by=By.XPATH, value=xpath_field)
    payment_field.clear()
    payment_field.send_keys("1111111111111111")
    
    # switch back to default content
    driver.switch_to.default_content()

