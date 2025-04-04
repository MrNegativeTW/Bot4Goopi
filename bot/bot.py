from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from utils.log import LogUtils
from data import constants as Constants

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("window-size=1400,1000")

def open_browser(shopline_product_link):
    opts = Options()
    opts.add_argument("--remote-debugging-port=9222")
    opts.add_experimental_option("detach", True)
    opts.add_argument("--user-data-dir=C:/selenium/GoopiChromeProfile")
    opts.add_argument("window-size=1300,1000")

    driver = webdriver.Chrome(options = opts)
    driver.get(shopline_product_link)


def launch_bot_from_product(shopline_product_link, customer_info):
    # Attach to existing browser
    opts = Options()
    opts.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=opts)
    if driver.current_url != shopline_product_link:
        driver.get(shopline_product_link)

    if p_product_fill(driver, customer_info) == False:
        return

    # Page: Cart
    if p_cart_fill(driver) == False:
        navigate_to_checkout_directly(driver)

    # Page: Checkout, fill payment and recipient info, etc.
    p_checkout_fill_recipient_form(driver, customer_info) # 這邊我們反過來先寫 7-11 地址
    p_checkout_fill_customer_info_form(driver, customer_info)
    p_checkout_fill_payment_form(driver, customer_info)
    p_checkout_fill_agree_box(driver)


def launch_bot_from_cart(customer_info):
    # Attach to existing browser
    opts = Options()
    opts.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(options=opts)
    if driver.current_url != Constants.URL_GOOPI_CART:
        driver.get(Constants.URL_GOOPI_CART)

    # Page: Cart
    if p_cart_fill(driver) == False:
        navigate_to_checkout_directly(driver)

    # Page: Checkout, fill payment and recipient info, etc.
    p_checkout_fill_recipient_form(driver, customer_info) # 這邊我們反過來先寫 7-11 地址
    p_checkout_fill_customer_info_form(driver, customer_info)
    p_checkout_fill_payment_form(driver, customer_info)
    p_checkout_fill_agree_box(driver)

# [START] 商品頁 ================================================================

def p_product_fill(driver, customer_info):
    """
    TODO: 用 xpath 找太不穩定了，要想辦法 parse 內容

    Page: 產品詳細頁 Products. 
    
    Url: www.goopi.co/products/*

    Select variations such as color, size, and quantity.

    Return: True if select variants successfully, False otherwise.
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
    is_product_select_success = True

    # [START] Color
    color_selected = customer_info['prod_color']
    if color_selected != "NA":
        xpath_color = xpath_variation_detail_prefix + str(div_index) + \
            xpath_color_suffix_1 + color_selected + xpath_color_suffix_2
        try:
            driver.find_element(By.XPATH, xpath_color).click()
            div_index += 1
        except Exception as e:
            is_product_select_success = False
            LogUtils.log_warn(f"[商品頁] 選擇\"顏色\"時錯誤\n{e}")
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
            is_product_select_success = False
            LogUtils.log_warn(f"[商品頁] 選擇\"尺寸\"時錯誤\n{e}")
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
            LogUtils.log_warn(f"[商品頁] 設定\"數量\"時錯誤\n{e}")
    # [END] Qty

    try:
        xpath_buyNow = "//*[@id=\"#btn-variable-buy-now\"]"
        driver.find_element(By.XPATH, xpath_buyNow).click()
    except Exception as e:
        is_product_select_success = False
        LogUtils.log_warn(f"[商品頁] 點選購買時錯誤，請確認購買的商品庫存")
    
    return is_product_select_success

def p_product_fill_new(driver, customer_info):
    xpath_buyNow = "//*[@id=\"#btn-variable-buy-now\"]"
    driver.find_element(By.XPATH, xpath_buyNow).click()

# [END] 商品頁 ==================================================================

# [START] 購物車 ================================================================

def p_cart_fill(driver):
    """
    Page: 購物車 Cart.

    Url: www.goopi.co/cart

    Returns: True if 前往結帳 clicked successfully, False otherwise.
    """
    xpath_goto_check = ".//a[contains(@href, \"/checkout\")]"
    max_attempts = 3  # Maximum retry attempts
    attempt = 0

    while attempt < max_attempts:
        try:
            attempt += 1
            LogUtils.log_info(f"[購物車] 第 {attempt} 次嘗試尋找 '前往結帳'")

            go_checkout_button = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, xpath_goto_check))
            )
            go_checkout_button.click()
            return True
        except Exception as e:
            LogUtils.log_warn(f"[購物車] Attempt {attempt} failed to locate '前往結帳' button. Error: {e}")
            
            if attempt < max_attempts:
                LogUtils.log_info(f"[購物車] 找不到，重整頁面 ({attempt + 1})")
                driver.refresh()
            else:
                LogUtils.log_warn(f"[購物車] 點選 \"前往結帳\"時錯誤\n{e}")
                return False

    return False

def navigate_to_checkout_directly(driver):
    """
    若於購物車頁面點擊「前往結帳」時錯誤，直接切換至 /checkout
    
    TODO: 不知道會不會有問題?
    """
    driver.get(Constants.URL_GOOPI_CHECKOUT)

# [END] 購物車 ==================================================================

def p_checkout_fill_customer_info_form(driver, customer_info):
    """
    Page: Checkout

    顧客資料
    """
    xpath_customer_name = "//*[@id=\"order-customer-name\"]"
    xpath_customer_mail = "//*[@id=\"order-customer-email\"]"
    xpath_customer_phone = "//*[@id=\"order-customer-phone\"]"
    xpath_line_id = "//*[@id=\"user-field-598198f2d4e395db79000a21\"]"
    name_customer_name = "order[customer_name]"
    name_customer_mail = "order[customer_email]"
    name_customer_phone = "order[customer_phone]"
    name_line_id = "saveFields[customer_info][598198f2d4e395db79000a21]"
    
    try:
        # customer_name_field = driver.find_element(by=By.XPATH, value=xpath_customer_name)
        customer_name_field = driver.find_element(by=By.NAME, value=name_customer_name)
        customer_name_field.clear()
        customer_name_field.send_keys(customer_info['name'])
    except Exception as e:
        LogUtils.log_warn(f"[顧客資料] 填寫顧客名稱時發生錯誤: {e}")
    
    try:
        # customer_mail_field = driver.find_element(by=By.XPATH, value=xpath_customer_mail)
        customer_mail_field = driver.find_element(by=By.NAME, value=name_customer_mail)
        customer_mail_field.clear()
        customer_mail_field.send_keys(customer_info['email'])
    except Exception as e:
        LogUtils.log_warn(f"[顧客資料] 填寫 email 時發生錯誤: {e}")

    try:
        # customer_phone_field = driver.find_element(by=By.XPATH, value=xpath_customer_phone)
        customer_phone_field = driver.find_element(by=By.NAME, value=name_customer_phone)
        customer_phone_field.clear()
        customer_phone_field.send_keys(customer_info['phone'])
    except Exception as e:
        LogUtils.log_warn(f"[顧客資料] 填寫電話時發生錯誤: {e}")

    try:
        # line_id_field = driver.find_element(by=By.XPATH, value=xpath_line_id)
        line_id_field = driver.find_element(by=By.NAME, value=name_line_id)
        line_id_field.clear()
        line_id_field.send_keys(customer_info['line_id'])
    except Exception as e:
        LogUtils.log_warn(f"[顧客資料] 填寫 LINE ID 時發生錯誤: {e}")


def p_checkout_fill_recipient_form(driver, customer_info):
    """
    Page: Checkout

    送貨資料: 姓名與電話
    """
    xpath_recipient_name = "//*[@id=\"recipient-name\"]"
    xpath_recipient_phone = "//*[@id=\"recipient-phone\"]"
    name_recipient_name = "order[delivery_data][recipient_name]"
    name_recipient_phone = "order[delivery_data][recipient_phone]"

    try:
        # recipient_name_field = driver.find_element(by=By.XPATH, value=xpath_recipient_name)
        recipient_name_field = driver.find_element(by=By.NAME, value=name_recipient_name)
        recipient_name_field.clear()
        recipient_name_field.send_keys(customer_info['name'])
    except Exception as e:
        LogUtils.log_warn(f"[送貨資料] 填寫名稱時發生錯誤: {e}")

    try:
        # recipient_phone_field = driver.find_element(by=By.XPATH, value=xpath_recipient_phone)
        recipient_phone_field = driver.find_element(by=By.NAME, value=name_recipient_phone)
        recipient_phone_field.clear()
        recipient_phone_field.send_keys(customer_info['phone'])
    except Exception as e:
        LogUtils.log_warn(f"[送貨資料] 填寫電話號碼時發生錯誤: {e}")

    p_checkout_fill_recipient_form_2(driver, customer_info)

def p_checkout_fill_recipient_form_2(driver, customer_info):
    """
    Page: Checkout

    送貨資料: 7-11 門市
    """
    id_select_seven = "seven-eleven-address" # 搜尋門市按鈕
    id_by_id = "byID" # Tabber 門市店號
    id_store_id_key = "storeIDKey"
    xpath_id_result = "//*[@id=\"ol_stores\"]/li[1]"
    id_seven_data = "sevenDataBtn" # 門市確認
    xpath_accept_btn = "//*[@id=\"AcceptBtn\"]" # 同意自助取件
    xpath_final_confirm = "//*[@id=\"submit_butn\"]" # 取貨地點確認

    try:
        driver.find_element(by=By.ID, value=id_select_seven).click()
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 點選 \"選擇門市\"\n{e}")

    try:
        by_id_tabber = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id_by_id))
        )
        by_id_tabber.click()
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 點選\"門市店號\"時錯誤\n{e}")

    # 7-11 會換 iframe

    # 切換至 iframe 內並送出門市店號
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "frmMain"))
        )
        store_id_field = driver.find_element(by=By.ID, value=id_store_id_key)
        store_id_field.clear()
        store_id_field.send_keys(customer_info['seven_id'])
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 填寫\"門市店號\"時錯誤\n{e}")

    # 點選搜尋門市
    try:
        js = "getStore();"
        driver.execute_script(js)
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 執行 getStore() 時錯誤\n{e}")
    
    # 點選搜尋結果的第一個
    try:
        # Wait for and click on the search result
        id_search_result = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_id_result))
        )
        id_search_result.click()
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 選擇第一個門市時發生錯誤\n{e}")
    finally:
        driver.switch_to.default_content()

    try:
        seven_data_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, id_seven_data))
        )
        seven_data_button.click()
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 點選\"門市確認\"時錯誤\n{e}")

    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_accept_btn))
        )
        # accept_button.click()
        js = "sendSeven()"
        driver.execute_script(js)
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 點選取貨不付款的\"同意\"時錯誤\n{e}")

    try:
        final_confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_final_confirm))
        )
        # final_confirm_button.click()
        js = "SendStore()"
        driver.execute_script(js)
    except Exception as e:
        LogUtils.log_warn(f"[711 門市] 點選取貨地點確認\"確認\"時錯誤\n{e}")    

def p_checkout_fill_payment_form(driver, customer_info):
    """
    Page: Checkout

    填寫付款資料, iframe 依序為卡號、持卡人姓名、有效期、安全碼
    """

    try:
        form = driver.find_element(By.ID, "checkout-shopline-payment-v2-form")
        iframes = form.find_elements(By.TAG_NAME, "iframe")
        LogUtils.log_info(f"[付款資料] 信用卡表單檢測到 {len(iframes)} 個 iframe")
    except Exception as e:
        LogUtils.log_warn("[付款資料] 找不到信用卡表單", f"錯誤: {e}")

    # Define the mapping of iframe names to customer_info fields
    field_mapping = {
        "number": "cc_number",
        "firstName": "cc_name",
        "expDate": "cc_date",
        "cvc": "cc_cvc"
    }

    for index, iframe in enumerate(iframes):
        try:
            frame_id = iframe.get_attribute('id')
            LogUtils.log_info(f"切換到 iframe - index: {index}, id: {frame_id}")
            driver.switch_to.frame(frame_id)

            input_element = driver.find_element(By.TAG_NAME, "input")
            matching_key = next((key for key in field_mapping if key in frame_id), None)
            if matching_key:
                input_element = driver.find_element(By.TAG_NAME, "input")
                input_value = customer_info.get(field_mapping[matching_key], "")
                input_element.send_keys(input_value)
                LogUtils.log_info(f"[付款資料] 輸入 {field_mapping[matching_key]}...")
            else:
                LogUtils.log_warn(f"[付款資料] 未知的 iframe id: {frame_id}")
        except Exception as e:
            LogUtils.log_warn(f"[付款資料] 填寫時發生錯誤 (index {index}, {frame_id})\n{e}")
        finally:
            driver.switch_to.default_content()

def p_checkout_fill_agree_box(driver):
    """
    Page: Checkout

    我同意網站服務條款及隱私權政策
    """

    try:
        js = "document.querySelector('input[name=\"policy\"]').click();"
        driver.execute_script(js)
    except Exception as e:
        LogUtils.log_warn(f"勾選同意條款時發生錯誤: {e}")

    xpath_agree_box = "//*[@id=\"checkout-container\"]/div/div[5]/div[1]/form/div/label/input"

    try:
        box = driver.find_element(by=By.XPATH, value=xpath_agree_box)
        if box.is_selected() == False:
            LogUtils.log_info("TODO(顯示未勾選訊息)")
    except Exception as e:
        LogUtils.log_warn("oops")
