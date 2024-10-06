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

    # # Page: Checkout, fill payment and recipient info, etc.
    p_checkout_fill_customer_info_form(driver, customer_info)
    p_checkout_fill_recipient_form(driver, customer_info)
    # p_checkout_fill_payment_form(driver, customer_info)
    # p_checkout_fill_agree_box(driver)


def p_product_fill(driver, customer_info):
    """
    Page: Products

    Select variations such as color, size, and quantity.
    """
    # xpaht_size = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[2]/select"
    # xpaht_size = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/select"
    # xpath_qty = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[2]/div/input"
    # xpath_qty = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div[3]/div[2]/div/input"
    
    xpath_variation_detail_prefix = "//*[@id=\"Content\"]/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div["

    xpath_color_suffix_1 = "]/div[2]/variation-selector/div/div["
    xpath_color_suffix_2 = "]"
    xpath_size_suffix = "]/div[2]/select"
    xpath_qty_suffix = "]/div[2]/div/input"

    div_index = 1 # Initialize index for dynamic divs

    # [START] Color
    color_selected = customer_info['prod_color']
    if color_selected != "NA":
        xpath_color = xpath_variation_detail_prefix + str(div_index) + \
            xpath_color_suffix_1 + color_selected + xpath_color_suffix_2
        try:
            driver.find_element(By.XPATH, xpath_color).click()
            div_index += 1
        except Exception as e:
            print(f"Error selecting color: {e}")
    # [END] Color

    # [START] Size
    size_selected = customer_info['prod_size']
    if size_selected != "NA":
        xpath_size = xpath_variation_detail_prefix + str(div_index) + xpath_size_suffix
        try:
            prod_size_field = Select(driver.find_element(by=By.XPATH, value=xpath_size))
            prod_size_field.select_by_visible_text(size_selected)
            div_index += 1
        except Exception as e:
            print(f"Error selecting size: {e}")
    # [END] Size

    # [START] Qty
    quantity = customer_info['prod_qty']
    if int(quantity) > 0:
        xpath_qty = xpath_variation_detail_prefix + str(div_index) + xpath_qty_suffix
        try:
            prod_qty_field = driver.find_element(by=By.XPATH, value=xpath_qty)
            prod_qty_field.clear()
            prod_qty_field.send_keys(quantity)
        except Exception as e:
            print(f"Error setting quantity: {e}")
    # [END] Size

    xpath_buyNow = "//*[@id=\"#btn-variable-buy-now\"]"
    driver.find_element(By.XPATH, xpath_buyNow).click()


def p_cart_fill(driver):
    """
    Page: Cart

    Don't use explicit waiting.
    """
    time.sleep(3) # TODO: Fix this shit looks toooo fucking stupid
    xpath_goCheckout = "//*[@id=\"checkout-container\"]/div/div[3]/div[4]/div[2]/section/div[2]/a"
    go_checkout_button = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, xpath_goCheckout))
    )
    go_checkout_button.click()


def p_checkout_fill_customer_info_form(driver, customer_info):
    """
    Page: Checkout

    顧客資料
    """
    xpath_customer_name = "//*[@id=\"order-customer-name\"]"
    xpath_customer_mail = "//*[@id=\"order-customer-email\"]"
    xpath_customer_phone = "//*[@id=\"order-customer-phone\"]"
    xpath_line_id = "//*[@id=\"user-field-598198f2d4e395db79000a21\"]"
    
    try:
        customer_name_field = driver.find_element(by=By.XPATH, value=xpath_customer_name)
        customer_name_field.clear()
        customer_name_field.send_keys(customer_info['name'])
    except Exception as e:
        print(f"Error filling name: {e}")
    
    try:
        customer_mail_field = driver.find_element(by=By.XPATH, value=xpath_customer_mail)
        customer_mail_field.clear()
        customer_mail_field.send_keys(customer_info['email'])
    except Exception as e:
        print(f"Error filling email: {e}")

    try:
        customer_phone_field = driver.find_element(by=By.XPATH, value=xpath_customer_phone)
        customer_phone_field.clear()
        customer_phone_field.send_keys(customer_info['phone'])
    except Exception as e:
        print(f"Error filling phone: {e}")

    try:
        line_id_field = driver.find_element(by=By.XPATH, value=xpath_line_id)
        line_id_field.clear()
        line_id_field.send_keys(customer_info['line_id'])
    except Exception as e:
        print(f"Error filling LINE ID: {e}")


def p_checkout_fill_recipient_form(driver, customer_info):
    """
    Page: Checkout

    送貨資料: 姓名與電話
    """
    xpath_recipient_name = "//*[@id=\"recipient-name\"]"
    xpath_recipient_phone = "//*[@id=\"recipient-phone\"]"
    xpath_select_seven = "//*[@id=\"seven-eleven-address\"]/div/div"

    try:
        recipient_name_field = driver.find_element(by=By.XPATH, value=xpath_recipient_name)
        recipient_name_field.clear()
        recipient_name_field.send_keys(customer_info['name'])
    except Exception as e:
        print(f"Error filling recipient name: {e}")

    try:
        recipient_phone_field = driver.find_element(by=By.XPATH, value=xpath_recipient_phone)
        recipient_phone_field.clear()
        recipient_phone_field.send_keys(customer_info['phone'])
    except Exception as e:
        print(f"Error filling recipient phone: {e}")

    try:
        driver.find_element(by=By.XPATH, value=xpath_select_seven).click()
    except Exception as e:
        print(f"Error clicking select seven button: {e}")

    p_checkout_fill_recipient_form_2(driver, customer_info)


def p_checkout_fill_recipient_form_2(driver, customer_info):
    """
    Page: Checkout

    送貨資料: 7-11 門市
    """
    xpath_by_id = "//*[@id=\"byID\"]" # Tabber 門市店號
    xpath_id_field = "//*[@id=\"storeIDKey\"]"
    xpath_id_search = "//*[@id=\"send\"]"
    xpath_id_result = "//*[@id=\"ol_stores\"]/li[1]"
    xpath_seven_data = "//*[@id=\"sevenDataBtn\"]" # 門市確認
    xpath_accept_btn = "//*[@id=\"AcceptBtn\"]" # 同意自助取件
    xpath_final_confirm = "//*[@id=\"submit_butn\"]" # 取貨地點確認

    try:
        by_id_tabber = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_by_id))
        )
        by_id_tabber.click()
    except Exception as e:
        print(f"選擇門市店號按鈕時發生錯誤: {e}")

    try:
        seven_id_field = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_id_field))
        )
        seven_id_field.clear()
        seven_id_field.send_keys(customer_info['seven_id'])
    except Exception as e:
        print(f"填寫門市店號時發生錯誤: {e}")

    try:
        id_search_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_id_search))
        )
        id_search_button.click()

        # Wait for and click on the search result
        id_search_result = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_id_result))
        )
        id_search_result.click()

        driver.find_element(by=By.XPATH, value=xpath_id_result).click()
        seven_data_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_seven_data))
        )
        seven_data_button.click()

        accept_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_accept_btn))
        )
        accept_button.click()
        
        final_confirm_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, xpath_final_confirm))
        )
        final_confirm_button.click()
    except Exception as e:
        print(f"搜尋門市店號後發生錯誤: {e}")
    

def p_checkout_fill_payment_form(driver, customer_info):
    """
    Page: Checkout

    付款資料
    """
    print("TODO")


def p_checkout_fill_agree_box(driver):
    """
    Page: Checkout

    我同意網站服務條款及隱私權政策
    """
    xpath_agree_box = "//*[@id=\"checkout-container\"]/div/div[5]/div[1]/form/div/label/input"
    try:
        driver.find_element(by=By.XPATH, value=xpath_agree_box).click()
    except Exception as e:
        print(f"Error checking agress to terms and conditions: {e}")