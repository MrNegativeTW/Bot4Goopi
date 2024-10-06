import tkinter as tk
from tkinter import messagebox, font, StringVar
from bot.bot import launch_bot, open_sign_in_page
from PIL import Image, ImageTk

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Goopi Bot - v0.0.1")
        self.setupWindow()

        self.createMenu()
        # self.createImages()

        self.createSectionBasic()
        self.createSectionDeliver()
        self.createSectionCreditCard()

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

        self.resizable(False, False)

    def createMenu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)
        menu.add_command(label='檔案')
        menu.add_command(label='載入上次資料')
        menu.add_command(label='儲存資料')

    def createImages(self):
        banner = Image.open('res/goopi_bot.png') 
        bannerPhotoImage  = ImageTk.PhotoImage(banner)

        icon_label = tk.Label(self, image=bannerPhotoImage)
        icon_label.grid(row=0, column=0, columnspan=2)
        icon_label.image = bannerPhotoImage

    def createSectionBasic(self):
        font_title = font.Font(family="Helvetica", size=12, weight="bold")
        font_entry =  font.Font(family="Helvetica", size=12)

        self.start_button = tk.Button(self, text="開啟瀏覽器", width=12, command=self.open_sign_in_page)
        self.start_button.grid(row=0, column=0)
        self.start_button = tk.Button(self, text="執行", width=12, command=self.start_bot_action)
        self.start_button.grid(row=0, column=1)

        tk.Label(self, text="商品網址", font=font_title).grid(row=1, column=0)
        self.entry_link = tk.Entry(self, font=font_entry)
        self.entry_link.insert(tk.END, "https://www.goopi.co/products/%E2%80%9Crve-s3%E2%80%9D-riverside-track-shorts-pure-black")
        self.entry_link.grid(row=1, column=1)
        self.button_clear_link = tk.Button(self, text=" 清除 ", command=self.clear_link_entry)
        self.button_clear_link.grid(row=1, column=3, padx=4)

        tk.Label(self, text="顏色", font=font_title).grid(row=2, column=0)
        options_c = ["NA", "1", "2", "3", "4", "5", "6"]
        self.prod_color_clicked = StringVar()
        self.prod_color_clicked.set(options_c[0])
        self.prod_color = tk.OptionMenu(self , self.prod_color_clicked , *options_c)
        self.prod_color.grid(row=2, column=1)

        tk.Label(self, text="尺寸", font=font_title).grid(row=3, column=0)
        options_s = ["NA", "1號", "2號", "3號", "4號", "S", "M", "L", "XL"]
        self.prod_size_clicked = StringVar()
        self.prod_size_clicked.set(options_s[0])
        self.prod_size = tk.OptionMenu(self , self.prod_size_clicked , *options_s)
        self.prod_size.grid(row=3, column=1)

        tk.Label(self, text="數量", font=font_title).grid(row=4, column=0)
        self.prod_qty = tk.Entry(self, font=font_entry, width=6)
        self.prod_qty.insert(tk.END, "1")
        self.prod_qty.grid(row=4, column=1)

        tk.Label(self, text="姓名", font=font_title).grid(row=5, column=0)
        self.entry_name = tk.Entry(self, font=font_entry)
        self.entry_name.insert(tk.END, "王大明")
        self.entry_name.grid(row=5, column=1)

        tk.Label(self, text="Email", font=font_title).grid(row=6, column=0)
        self.entry_email = tk.Entry(self, font=font_entry)
        self.entry_email.insert(tk.END, "example@example.com")
        self.entry_email.grid(row=6, column=1)

        tk.Label(self, text="電話", font=font_title).grid(row=7, column=0)
        self.entry_phone = tk.Entry(self, font=font_entry)
        self.entry_phone.insert(tk.END, "0800092000")
        self.entry_phone.grid(row=7, column=1)

        tk.Label(self, text="Line ID", font=font_title).grid(row=8, column=0)
        self.entry_line_id = tk.Entry(self, font=font_entry)
        self.entry_line_id.insert(tk.END, "asdasdasd")
        self.entry_line_id.grid(row=8, column=1)

    def clear_link_entry(self):
        self.entry_link.delete(0, tk.END)

    def createSectionDeliver(self):
        font_title = font.Font(family="Helvetica", size=12, weight="bold")
        font_entry =  font.Font(family="Helvetica", size=12)

        tk.Label(self, text="取貨門市 TODO", font=font_title).grid(row=10, column=0)

    def createSectionCreditCard(self):
        font_title = font.Font(family="Helvetica", size=12, weight="bold")
        font_entry =  font.Font(family="Helvetica", size=12)

        tk.Label(self, text="信用卡號(無空格)", font=font_title).grid(row=20, column=0)
        self.cc_number = tk.Entry(self, font=font_entry)
        self.cc_number.insert(tk.END, "4037200875496790")
        self.cc_number.grid(row=20, column=1)

        tk.Label(self, text="到期年月(無斜線)", font=font_title).grid(row=21, column=0)
        self.cc_date = tk.Entry(self, font=font_entry)
        self.cc_date.insert(tk.END, "1229")
        self.cc_date.grid(row=21, column=1)

        tk.Label(self, text="安全碼", font=font_title).grid(row=22, column=0)
        self.cc_cvc = tk.Entry(self, font=font_entry)
        self.cc_cvc.insert(tk.END, "777")
        self.cc_cvc.grid(row=22, column=1)

        tk.Label(self, text="持卡人姓名", font=font_title).grid(row=23, column=0)
        self.cc_name = tk.Entry(self, font=font_entry)
        self.cc_name.insert(tk.END, "王大明")
        self.cc_name.grid(row=23, column=1)

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

    
