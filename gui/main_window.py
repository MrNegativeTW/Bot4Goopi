import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, font, StringVar
from bot.bot import launch_bot, open_sign_in_page
from PIL import Image, ImageTk

from data import constants as Constants

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Goopi Bot - v0.0.1")
        self.setupWindow()

        # self.createMenu()
        # self.createImages()
        self.create_notebook()
        self.create_section_pref()
        self.create_section_autofill()
        self.create_section_about()

        self.create_footer_actions()

    def setupWindow(self):
        w = 400 # width for the Tk root
        h = 400 # height for the Tk root
        # get screen width and height
        ws = self.winfo_screenwidth() # width of the screen
        hs = self.winfo_screenheight() # height of the screen
        # calculate x and y coordinates for the Tk root window
        # x = (ws / 2) - (w / 2)
        # y = (hs / 2) - (h / 2) - 160
        x = ws - w - 10
        y = 80
        # set the dimensions of the screen 
        # and where it is placed
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # self.resizable(False, False)

    def createMenu(self):
        menu = tk.Menu(self)
        menu.add_command(label='載入資料')
        menu.add_command(label='儲存資料')
        menu.add_command(label='注意事項', command=self.show_info_dialog)
        menu.add_command(label='關於', command=self.show_about_dialog)
        self.config(menu=menu)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self, width=300)
        self.notebook.grid(row=0, column=0)

    def add_notebook(self, frame, title):
        self.notebook.add(frame, text=title)

    def create_section_pref(self):
        frame1 = tk.Frame()
        font_title = font.Font(family="Helvetica", size=10)
        font_entry =  font.Font(family="Helvetica", size=10)

        tk.Label(frame1, text="商品網址", font=font_title).grid(row=1, column=0)
        self.entry_link = tk.Entry(frame1, font=font_entry, width=30)
        self.entry_link.insert(tk.END, "https://www.goopi.co/products/%E2%80%9Crve-s3%E2%80%9D-riverside-track-shorts-pure-black")
        self.entry_link.grid(row=1, column=1)

        tk.Label(frame1, text="顏色", font=font_title, justify="right").grid(row=2, column=0)
        options_c = ["NA", "1", "2", "3", "4", "5", "6"]
        self.prod_color_clicked = StringVar()
        self.prod_color_clicked.set(options_c[0])
        prod_color = tk.OptionMenu(frame1 , self.prod_color_clicked , *options_c)
        prod_color.grid(row=2, column=1)

        tk.Label(frame1, text="尺寸", font=font_title, justify="right").grid(row=3, column=0)
        options_s = ["NA", "1號", "2號", "3號", "4號", "S", "M", "L", "XL"]
        self.prod_size_clicked = StringVar()
        self.prod_size_clicked.set(options_s[0])
        prod_size = tk.OptionMenu(frame1 , self.prod_size_clicked , *options_s)
        prod_size.grid(row=3, column=1)

        tk.Label(frame1, text="數量", font=font_title, justify="right").grid(row=4, column=0)
        self.prod_qty = tk.Entry(frame1, font=font_entry, width=6)
        self.prod_qty.insert(tk.END, "1")
        self.prod_qty.grid(row=4, column=1)

        box = ttk.Combobox(frame1, width=15, values=Constants.CONST_SIZE_LIST)
        box.grid(row=5, column=1)
        box.current(0)
        # 改用這個box.current() box.get()

        frame1.button_clear_link = tk.Button(frame1, text="清除全部", command=self.clear_link_entry)
        frame1.button_clear_link.grid(row=9, column=0, padx=4)

        self.add_notebook(frame1, "偏好設定")

    def clear_link_entry(self):
        self.entry_link.delete(0, tk.END)

    def create_section_autofill(self):
        frame = tk.Frame()
        font_area_start = font.Font(family="Helvetica", size=10, weight="bold")
        font_title = font.Font(family="Helvetica", size=10)
        font_entry =  font.Font(family="Helvetica", size=10)

        tk.Label(frame, text="基本資料", font=font_area_start).grid(row=1, column=0)

        tk.Label(frame, text="姓名", font=font_title).grid(row=5, column=0)
        self.entry_name = tk.Entry(frame, font=font_entry)
        self.entry_name.insert(tk.END, "王大明")
        self.entry_name.grid(row=5, column=1)

        tk.Label(frame, text="Email", font=font_title).grid(row=6, column=0)
        self.entry_email = tk.Entry(frame, font=font_entry)
        self.entry_email.insert(tk.END, "example@example.com")
        self.entry_email.grid(row=6, column=1)

        tk.Label(frame, text="電話", font=font_title).grid(row=7, column=0)
        self.entry_phone = tk.Entry(frame, font=font_entry)
        self.entry_phone.insert(tk.END, "0800092000")
        self.entry_phone.grid(row=7, column=1)

        tk.Label(frame, text="Line ID", font=font_title).grid(row=8, column=0)
        self.entry_line_id = tk.Entry(frame, font=font_entry)
        self.entry_line_id.insert(tk.END, "asdasdasd")
        self.entry_line_id.grid(row=8, column=1)

        tk.Label(frame, text="送貨資訊", font=font_area_start).grid(row=11, column=0)
        tk.Label(frame, text="門市店號", font=font_title).grid(row=12, column=0)
        self.seven_id = tk.Entry(frame, font=font_entry)
        self.seven_id.insert(tk.END, "254063")
        self.seven_id.grid(row=12, column=1)

        tk.Label(frame, text="信用卡資料", font=font_area_start).grid(row=21, column=0)
        tk.Label(frame, text="信用卡號(無空格)", font=font_title).grid(row=22, column=0)
        self.cc_number = tk.Entry(frame, font=font_entry)
        self.cc_number.insert(tk.END, "4037200875496790")
        self.cc_number.grid(row=22, column=1)

        tk.Label(frame, text="到期年月(無斜線)", font=font_title).grid(row=23, column=0)
        self.cc_date = tk.Entry(frame, font=font_entry)
        self.cc_date.insert(tk.END, "1229")
        self.cc_date.grid(row=23, column=1)

        tk.Label(frame, text="安全碼", font=font_title).grid(row=24, column=0)
        self.cc_cvc = tk.Entry(frame, font=font_entry)
        self.cc_cvc.insert(tk.END, "777")
        self.cc_cvc.grid(row=24, column=1)

        tk.Label(frame, text="持卡人姓名", font=font_title).grid(row=25, column=0)
        self.cc_name = tk.Entry(frame, font=font_entry)
        self.cc_name.insert(tk.END, "王大明")
        self.cc_name.grid(row=25, column=1)

        self.add_notebook(frame, "自動填入")

    def create_section_about(self):
        frame = tk.Frame()
        banner = Image.open('res/goopi_bot.png') 
        bannerPhotoImage  = ImageTk.PhotoImage(banner)

        icon_label = tk.Label(frame, image=bannerPhotoImage)
        icon_label.grid(row=0, column=0, columnspan=2)
        icon_label.image = bannerPhotoImage
        self.add_notebook(frame, "關於")

    def create_footer_actions(self):
        self.start_button = tk.Button(self, text="開啟瀏覽器", width=12, command=self.open_sign_in_page)
        self.start_button.grid(row=2, column=0, pady=8)
        self.start_button = tk.Button(self, text="執行", width=12, command=self.start_bot_action)
        self.start_button.grid(row=2, column=1, pady=8)

    def open_sign_in_page(self):
        open_sign_in_page()

    def start_bot_action(self):
        customer_info = {
            'prod_color': self.prod_color_clicked.get(),
            'prod_size': self.prod_size_clicked.get(),
            'prod_qty': self.prod_qty.get(),
            'name': self.entry_name.get(),
            'email': self.entry_email.get(),
            'phone': self.entry_phone.get(),
            'line_id': self.entry_line_id.get(),
            'seven_id': self.seven_id.get(),
            'cc_number': self.cc_number.get(),
            'cc_date': self.cc_date.get(),
            'cc_cvc': self.cc_cvc.get(),
            'cc_name': self.cc_name.get()
        }
        product_link = self.entry_link.get()

        if not all(customer_info.values()) or not product_link:
                messagebox.showerror("等等!", "請填寫所有資料!")
                return
        
        # You can pass the card number to your bot function
        # config = load_config()
        launch_bot(product_link, customer_info)
        # messagebox.showinfo("Success", "Bot started successfully!")

    
