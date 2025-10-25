from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from subprocess import Popen as popen
import shutil
import hashlib
import datetime
import os
import time
import json

class MsgBox:
    @staticmethod
    def _create_window(parent, title, icon_path, message, buttons, return_result=False):
        result = {"value": None} if return_result else None

        window = Toplevel(parent)
        window.overrideredirect(True)
        window.geometry("300x150+300+300")
        window.attributes("-topmost", True)

        # 假標題列
        title_bar = Frame(window, bg=bgc, height=30)
        title_bar.pack(fill="x")

        title_label = Label(title_bar, text=title, bg=bgc, fg=fgc, font=("微軟正黑體", 10))
        title_label.pack(side="left", padx=10)

        def start_move(event):
            window.x = event.x
            window.y = event.y

        def do_move(event):
            x = window.winfo_pointerx() - window.x
            y = window.winfo_pointery() - window.y
            window.geometry(f"+{x}+{y}")

        title_bar.bind("<Button-1>", start_move)
        title_bar.bind("<B1-Motion>", do_move)

        # 圖示
        icon_pict = PhotoImage(file=icon_path)
        icon = Label(window, image=icon_pict)
        icon.image = icon_pict
        icon.pack(pady=4)

        # 文字訊息
        Label(window, text=message, font=("微軟正黑體", 12)).pack(pady=2)

        # 按鈕區塊
        button_frame = Frame(window)
        button_frame.pack(pady=2)

        for text, value in buttons:
            def handler(v=value):
                if return_result:
                    result["value"] = v
                window.destroy()
            Button(button_frame, text=text, command=handler).pack(side="left", padx=10)

        if return_result:
            parent.wait_window(window)
            return result["value"]

    @staticmethod
    def error(parent, title, message):
        MsgBox._create_window(parent, title, "X:/bin/icons/error.png", message, [
            (" 確定 ", None)
        ])

    @staticmethod
    def warn(parent, title, message):
        MsgBox._create_window(parent, title, "X:/bin/icons/warn.png", message, [
            (" 確定 ", None)
        ])

    @staticmethod
    def info(parent, title, message):
        MsgBox._create_window(parent, title, "X:/bin/icons/info.png", message, [
            (" 確定 ", None)
        ])

    @staticmethod
    def ask(parent, title, message):
        return MsgBox._create_window(parent, title, "X:/bin/icons/ask.png", message, [
            (" 是 ", True),
            (" 否 ", False)
        ], return_result=True)

class SafeShutdown():
    def __init__(self, master):  # 添加 master 參數
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.icon = PhotoImage(file=r"X:\bin\icons\power.png")
        self.btn = Button(root, anchor='w',bg=bgc,fg=fgc,image=self.icon, command=self.focus_window)
        self.btn.image = self.icon #以防回收
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        log("[SafeShutdown] App bar button packed")
        
        self.window = Toplevel(root)
        self.window.title("shutdown")
        self.window.geometry("300x225+362+284")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        log(f"[SafeShutdown] Toplevel created")
        
        self.x_offset = 0
        self.y_offset = 0

        # 標題欄 Frame
        self.title_bar = Frame(self.window, bg=bgc, relief="raised", bd=0)
        self.title_bar.pack(fill="x")

        # 標題 Label
        self.title_label = Label(self.title_bar, text="關閉ShellyOS", bg=bgc, fg=fgc, font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        self.exit_btn = Button(self.title_bar, text="✕", command=self.exiting)
        self.exit_btn.pack(side="right")
        log("[SafeShutdown] Title bar packed")
        
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.change_color()
        
        # 標題文字
        self.label = Label(self.window, text="感謝使用ShellyOS!\n請問想讓電腦做甚麼？", font=("Microsoft JhengHei", 12))
        self.label.pack(pady=10)

        # 使用 ttk 的 Combobox 顯示下拉選單
        self.action_var = StringVar()  # 改為 self.action_var
        self.combo = ttk.Combobox(self.window, textvariable=self.action_var, state="readonly")  # 修正這裡
        self.combo['values'] = ("關機", "重新啟動", "鎖定")
        self.combo.current(0)  # 預設選第一個
        self.combo.pack(pady=5)
        
        # 確定按鈕
        self.confirm_button = Button(self.window, text="確定", width=6, height=1, command=self.execute_action)
        self.confirm_button.pack(pady=10)
        self.cancel_button = Button(self.window, text="取消", width=6, height=1, command=self.exiting)
        self.cancel_button.pack(pady=10)
        
        log(f"[SafeShutdown] Label, combo and buttons packed")
    
    def execute_action(self):
        action = self.action_var.get()
        if action == "關機":
            self._cleanup_and_shutdown()
        elif action == "重新啟動":
            self._cleanup_and_reboot()
        elif action == "鎖定":
            self._lock_system()
        else:
            MsgBox.info(self.window,"提示", "請選擇一個有效的選項")
            log(f"[SafeShutdown] Unusable chosen, returned")
    
    def _cleanup_and_shutdown(self):
        """清理並關機"""
        self._cleanup_apps()
        self.exiting()            
        bg.destroy()
        root.destroy()
        log(f"[SafeShutdown] System shutdown")
        popen("wpeutil shutdown")
    
    def _cleanup_and_reboot(self):
        """清理並重啟"""
        try:
            self._cleanup_apps()
            self.exiting()   
            bg.destroy()
            root.destroy()
            log(f"[SafeShutdown] System reboot")
            popen("wpeutil reboot")
        except:
            # 測試環境 fallback
            print(f"[SafeShutdown] Experiment environment, re-initializing...")
            time.sleep(3)
            initialization()
    
    def _lock_system(self):
        """鎖定系統"""
        LockScreen(root)
        self.exiting()
        log(f"[SafeShutdown] Lock screen activated")
    
    def _cleanup_apps(self):
        """清理所有運行中的應用"""
        for app in apps_running:
            try:
                app.exiting()
                log(f"[SafeShutdown] App {type(app).__name__} exited")
            except Exception as e:
                log(f"[SafeShutdown] Error exiting app: {e}")

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")
        
    def change_color(self):
        self.btn.config(bg=bgc, fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc, fg=fgc)
        self.exit_btn.config(bg=bgc, fg=fgc)
        
    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
    
    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        if self in apps_running:
            apps_running.remove(self)
        log("[SafeShutdown] Got exiting message, destroyed and removed from apps_running")
       
class LockScreen():
    def __init__(self, master):
        self.master = master
        root.attributes("-topmost", False)
        
        global locking, timer
        locking = True
        timer = 0.0
        
        self.window = Toplevel(root)
        self.window.title("ShellyOS Lock Screen")
        self.window.geometry("1024x768")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(background='#0078D4')
        log("[LockScreen]Toplevel created")
        # 載入 PNG 或 GIF 圖片
        self.bg_image = PhotoImage(file=lock_wall)

        # 設定 Label 為背景
        self.bg_label = Label(self.window, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        log("[LockScreen]Background applyed")
        self.time_label = Label(self.window,text="00:00",font=("微軟正黑體",30),bg=bgc,fg=fgc)
        self.time_label.pack(fill="x",side='top')
        self.date_label = Label(self.window, text="2000/01/01 (Sat)", font=("微軟正黑體", 16),bg=bgc,fg=fgc)
        self.date_label.pack(fill="x")
        log("[LockScreen]Time / date label packed")
        self.window.after(100, self.time_set)

        self.unlock_btn = Button(self.window,text="解鎖",font=("微軟正黑體",20),command=self.check_lock,bg=bgc,fg=fgc)
        self.unlock_btn.pack(fill="x",side='bottom')
        
        log("[LockScreen]Unlock button packed")
        self.window.protocol("WM_DELETE_WINDOW", disable_close)
        
    def check_lock(self):
        if saved_hash == "":
            self.unlock()
        else:
            self.password_window()
            self.unlock_btn.config(state="disabled")
    
    def unlock(self):
        global locking
        self.window.destroy()
        locking = False
        root.attributes("-topmost", True)
        log("[LockScreen]Got unlock message, destroyed")
    def time_set(self):
        now = datetime.datetime.now()
        fod = now.strftime("%Y/%m/%d (%a)")
        self.date_label.config(text=fod)
        fot = now.strftime("%H:%M")
        self.time_label.config(text=fot)
        self.window.after(1000, self.time_set)
    
    def check_password(self, password):
        if hashlib.sha256(password.encode('utf-8')).hexdigest() == saved_hash:
            self.pw_win.destroy()
            self.unlock()
        else:
            MsgBox.error(self.window,"錯誤","密碼錯誤，請再試一次")
            self.password_entry.delete(0, END)
            
    def password_window(self):
        self.pw_win = Toplevel(self.window) 
        self.pw_win.title("pw")
        self.pw_win.geometry("225x120+372+364")
        self.pw_win.attributes("-topmost", True)
        self.pw_win.overrideredirect(True)
        
        self.pw_title = Frame(self.pw_win,bg=bgc)
        self.pw_title.pack(fill="x")
        self.title_label = Label(self.pw_title, text="ShellyOS 安全性",bg=bgc,fg=fgc, font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        Label(self.pw_win, text="請輸入密碼：", font=("微軟正黑體", 12)).pack(pady=5)
        self.password_entry = Entry(self.pw_win,show="*")
        self.password_entry.pack()
        Button(self.pw_win, text="完成", command=lambda: self.check_password(self.password_entry.get())).pack(pady=2)
        
class About():
    def __init__(self, master):
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.icon = PhotoImage(file=r"X:\bin\icons\about.png")
        self.btn = Button(root, anchor='w',bg=bgc,fg=fgc,image=self.icon, command=self.focus_window)
        self.btn.image = self.icon #以防回收
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        
        log("[About]App bar button packed")
        
        self.window = Toplevel(master)
        self.window.title("about")
        self.window.geometry("400x300+100+100")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        log("[About]Toplevel created")
        
        self.x_offset = 0
        self.y_offset = 0
        
        self.title_bar = Frame(self.window, bg="#eeffff", relief="raised", bd=0)
        self.title_bar.pack(fill="x")
        
        self.title_label = Label(self.title_bar, text="關於 ShellyOS", bg="#eeffff", fg="black", font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        log("[About]Title bar packed")
        
        banner = PhotoImage(file="X:/bin/icons/aboutlogo.png")
        banner_label = Label(self.window, image=banner, bg=bgc)
        banner_label.image = banner
        banner_label.pack()

        Label(self.window,text="ShellyOS v.3.0.2333.38 未經授權可以轉載\n\n基於Windows 11 PE與Pyinstaller\n\nWindows、Windows PE和Aero Basic是\nMicrosoft Corp.的註冊商標", font=("微軟正黑體", 12)).pack(pady=5)
        log("[About]Contect labels packed")
        if os.path.isfile('C:\\Windows\\explorer.exe'):
            Label(self.window,text="目前正在測試", font=("微軟正黑體", 10)).pack(pady=5)
            log("[About]For test label packed")
        
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.change_color()
        Button(self.window,text="我知道了",width=6, height=1, font=("微軟正黑體", 12),command=self.exiting).pack(pady=5)
        log("[About]I knew button packed")
        self.window.protocol("WM_DELETE_WINDOW", disable_close)
        
    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")
    
    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
    
    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        apps_running.pop(self.myidx)
        log("[About]Got exiting message, destroyed and poped")  
    
    def change_color(self):
        self.btn.config(bg=bgc,fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc,fg=fgc)

class Calc():
    def __init__(self, master):
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.icon = PhotoImage(file=r"X:\bin\icons\calc.png")
        self.btn = Button(root, anchor='w',bg=bgc,fg=fgc,image=self.icon, command=self.focus_window)
        self.btn.image = self.icon #以防回收
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        log("[Calc]App bar button packed")
        
        self.window = Toplevel(root)
        self.window.title("計算機")
        self.window.geometry("200x248")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)    
        log("[Calc]Toplevel created")
        
        # 拖曳用偏移
        self.x_offset = 0
        self.y_offset = 0

        # 標題欄 Frame
        self.title_bar = Frame(self.window, bg="#eeffff", relief="raised", bd=0)
        self.title_bar.pack(fill="x")

        # 標題 Label
        self.title_label = Label(self.title_bar, text="計算機", bg="#eeffff", fg="black", font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        self.exit_btn = Button(self.title_bar, text="✕", command=self.exiting)
        self.exit_btn.pack(side="right")
        log("[Calc]Title bar packed")
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.change_color()
        
        self.entry = Entry(self.window, font=("微軟正黑體", 15), justify="right")
        self.entry.pack(padx=10, pady=10,fill="x")
        log("[Calc]Entry packed")
        
        self.content_frame = Frame(self.window)
        self.content_frame.pack(fill="both", expand=True)
        
        self.buttons = [
            ("%", 0, 0), ("C", 0, 1),("←", 0, 2),("/", 0, 3),
            ("7", 1, 0), ("8", 1, 1),("9", 1, 2),("*", 1, 3),
            ("4", 2, 0), ("5", 2, 1),("6", 2, 2),("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1),("3", 3, 2),("+", 3, 3),
            (".", 4, 0), ("0", 4, 1),("x²", 4, 2),("=", 4, 3),
        ]
        
        

        for (text, row, col) in self.buttons:
            if text == "C":
                cmd = self.clear
            elif text == "=":
                cmd = self.calculate
            elif text == "←":
                cmd = self.clslast
            else:
                cmd = lambda x=text: self.press(x)
            Button(self.content_frame, text=text, font=("微軟正黑體", 12), width=4, height=1, command=cmd).grid(row=row, column=col, sticky="nsew")
        log("[Calc]Buttons packed")
        self.window.protocol("WM_DELETE_WINDOW", disable_close)
    
    # 拖曳功能
    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")
        
    def change_color(self):
        self.btn.config(bg=bgc,fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc,fg=fgc)
        
    # Appbar 按鈕功能
    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
    
    def isInt(self,n):
        intn = 0
        try:
            intn = int(n)
            if float(intn) == n:
                return True
            else:
                return False
        except:
            return False

    def press(self,n):
        if n == "x²":
            self.entry.insert(END, "**2")
        else:self.entry.insert(END, str(n))

    def clear(self):
        self.entry.delete(0, END)

    def calculate(self):
        try:
            result = eval(self.entry.get())
            
            self.entry.delete(0, END)
            if self.isInt(result):
                self.entry.insert(END, str(int(result)))
            else:
                self.entry.insert(END, str(result))
            log("[Calc]Got calculate command and successed")
        except Exception as e:
            self.entry.delete(0, END)
            self.entry.insert(END, "錯誤")
            log(f"[Calc]Got calculate command ,but failed:{e}")

    def clslast(self):
        try:
            newentryget = self.entry.get()[:-1]
            self.entry.delete(0, END)
            self.entry.insert(END, newentryget)
        except:
            self.entry.delete(0, "end")
            
    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        apps_running.pop(self.myidx)
        log("[Calc]Got exiting message, destroyed and poped")

class Note():
    def __init__(self, master, filepath=""):
        self.myidx = len(apps_running)-1
        self.master = master
        self.file_path = filepath

        # 建立 Appbar 按鈕
        self.icon = PhotoImage(file=r"X:\bin\icons\notepad.png")
        self.btn = Button(root, anchor='w',bg=bgc,fg=fgc,image=self.icon, command=self.focus_window)
        self.btn.image = self.icon #以防回收
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        log("[Note]App bar button packed")
        
        # 建立記事本視窗
        self.window = Toplevel(master)
        self.window.title("記事本")
        self.window.geometry("600x400+100+100")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        log("[Note]Toplevel created")
        # 拖曳用偏移
        self.x_offset = 0
        self.y_offset = 0

        # 標題欄 Frame
        self.title_bar = Frame(self.window, bg="#eeffff", relief="raised", bd=0)
        self.title_bar.pack(fill="x")

        # 標題 Label
        self.title_label = Label(self.title_bar, text="記事本", bg="#eeffff", fg="black", font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)

        # File & Exit 按鈕
        Button(self.title_bar, text="✕", command=self.exiting).pack(side="right")
        Button(self.title_bar, text="檔案", command=self.show_file_menu).pack(side="right")
        log("[Note]Title bar packed")
        # 綁定拖曳事件
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.change_color()

        # Text 區域
        self.text_area = Text(self.window, font=("微軟正黑體", 14))
        self.text_area.pack(expand=True, fill="both")
        log("[Note]Text area packed")
        # 建立 Menu
        self.file_menu = Menu(self.window, tearoff=0)
        self.file_menu.add_command(label="開啟", command=self.open_file)
        self.file_menu.add_command(label="儲存", command=self.save_file)
        self.file_menu.add_command(label="另存新檔", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="退出", command=self.exiting)
        log("[Note]Menu packed")
        if self.file_path != "":
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_area.delete(1.0, END)
                self.text_area.insert(END, content)

        # 關閉事件
        self.window.protocol("WM_DELETE_WINDOW", disable_close)
        

    # 拖曳功能
    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")

    # Appbar 按鈕功能
    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    # File menu 顯示
    def show_file_menu(self):
        try:
            self.file_menu.tk_popup(self.window.winfo_rootx() + 500, self.window.winfo_rooty() + 25)
        finally:
            self.file_menu.grab_release()

    # 文件操作
    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("文字檔", "*.txt")])
        if self.file_path:
            with open(self.file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_area.delete(1.0, END)
                self.text_area.insert(END, content)
                log(f"[Note]File opened:{f}")

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, END))
                log(f"[Note]File saved:{f}")
        else:
            self.save_as()

    def save_as(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                      filetypes=[("文字檔", "*.txt")])
        if self.file_path:
            with open(self.file_path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get(1.0, END))
                log(f"[Note]File saved:{f}")

    def change_color(self):
        self.btn.config(bg=bgc,fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc,fg=fgc)

    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        apps_running.pop(self.myidx)
        log("[Note]Got exiting message, destroyed and poped")

class CommandLine:
    def __init__(self, master):
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.icon = PhotoImage(file=r"X:\bin\icons\command.png")
        self.btn = Button(root, anchor='w',bg=bgc,fg=fgc,image=self.icon, command=self.focus_window)
        self.btn.image = self.icon #以防回收
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        log("[Command]App bar button packed")
        
        self.window = Toplevel(root)
        self.window.title("ShellyOS 指令")
        self.window.geometry("600x300")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)    

        log("[Command]Toplevel created")
        # 拖曳用偏移
        self.x_offset = 0
        self.y_offset = 0

        # 標題欄 Frame
        self.title_bar = Frame(self.window, bg="#eeffff", relief="raised", bd=0)
        self.title_bar.pack(fill="x")

        # 標題 Label
        self.title_label = Label(self.title_bar, text="ShellyOS 指令", bg="#eeffff", fg="black", font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        self.exit_btn = Button(self.title_bar, text="✕", command=self.exiting)
        self.exit_btn.pack(side="right")
        log("[Command]Title bar created")
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        
        
        self.text_area = Text(self.window, font=("微軟正黑體", 12))
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<Return>", self.execute_command)
        
        self.change_color()
        helpcom = """
可用指令：
calc - 開啟計算器
note - 開啟記事本
about - 開啟關於介面
tls - 顯示目前所有進程
ver - 顯示版本資訊
cls - 清空列表
shutdown <s/r/l/g> - 執行電源選項
echo - 顯示輸入的內容
help - 顯示所有可用指令
"""
        self.command = ""
        self.commands = {
            "calc": lambda command: apps_running.append(Calc(root)),
            "note": lambda command: apps_running.append(Note(root)),
            "about": lambda command: apps_running.append(About(root)),
            "tls": lambda command: self.text_area.insert(END, f"\n目前執行中：{', '.join([type(app).__name__ for app in apps_running])}"),
            "ver": lambda command: self.text_area.insert(END, "\nShellyOS Terminal v.3.0.2333.38 未經授權可以轉載"),
            "cls": lambda command:self.text_area.delete(1.0, END),
            "shutdown": lambda command:self.shutdown_command(),
            "echo": lambda command:self.text_area.insert(END,"\n"+command[5:].strip()),
            "help": lambda command: self.text_area.insert(END, helpcom)
        }
        
        self.text_area.insert(END, "ShellyOS CLI > ")
        log("[Command]Text area packed")
        self.window.protocol("WM_DELETE_WINDOW", disable_close)
    
    def shutdown_command(self):
        argv = self.command[9:].strip()
        if argv == "s":
            for i in apps_running:
                idx = app_running.index(o)
                i.exiting()
                log(f"[Shutdown]Notice app {i} ({idx})exiting")
            log(f"[Shutdown]Destroyed self")            
            bg.destroy()
            log(f"[Shutdown]Destroyed background")
            root.destroy()
            log(f"[Shutdown]Destroyed root and trying shutdown")
            log_file.close()
            del log_file
            popen("wpeutil shutdown")
        elif argv == "r":
            try:
                for i in apps_running:
                    i.exiting()
                    log(f"[Shutdown]Notice app {i} ({idx})exiting")
                log(f"[Shutdown]Destroyed self")   
                bg.destroy()
                log(f"[Shutdown]Destroyed background")
                root.destroy()
                log(f"[Shutdown]Destroyed root and trying shutdown")
                log_file.close()
                del log_file
                popen("wpeutil reboot")
            except:
                print(f"[Init]Experiment envitment, will re-initialization after 3 seconds")
                time.sleep(3)
                initialization()
        elif argv == "l":
            LockScreen(root)
            log(f"[Shutdown]Called LockScreen and destroyed self")
        elif argv == "g":
            apps_running.append(SafeShutdown(root))
        else:
            self.text_area.insert(END, "\n s = 關機; r = 重啟; l = 鎖定; g = 顯示圖形介面")
            
            
    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")

    # Appbar 按鈕功能
    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
    
    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        apps_running.pop(self.myidx)
        log("[Command]Got exiting message, destroyed and poped")
        
    def change_color(self):
        self.btn.config(bg=bgc,fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc,fg=fgc)
        self.text_area.config(bg=bgc,fg=fgc)
        
    def execute_command(self, event):
        current_line_index = self.text_area.index("insert").split(".")[0]
        line_start = f"{current_line_index}.0"
        line_end = f"{current_line_index}.end"
        command = self.text_area.get(line_start, line_end).replace("ShellyOS CLI > ", "").strip()

        if command.split(" ")[0] in self.commands:
            self.commands[command.split(" ")[0]](command)
            log(f"[Command]Executed command: {command}")
        else:
            self.text_area.insert(END, f"\n未知指令：{command}")
            log(f"[Command]Returned unknowned message")

        # 加上新的提示字串
        lines = self.text_area.get("1.0", END).strip().split("\n")
        if len(lines) > 13:
            new_text = "\n".join(lines[-12:])  # 保留 12 行 + CLI 提示
            self.text_area.delete("1.0", END)
            self.text_area.insert("1.0", new_text)
        self.text_area.insert(END, "\nShellyOS CLI > ")

        
        # 阻止 Text widget 自動換行
        return "break"

class UpdateLog():
    def __init__(self, master):
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.icon = PhotoImage(file=r"X:\bin\icons\update.png")
        self.btn = Button(root, anchor='w',bg=bgc,fg=fgc,image=self.icon, command=self.focus_window)
        self.btn.image = self.icon #以防回收
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        
        self.logs = {
            "ver 3.0.2333.38":"[加入]工作列圖示\n[更新]加入經典、塗鴉主題\n[替換]更換訊息框樣式\n[更新]CLI可跟隨主題\n[更新]計算機介面更改\n[加入]自動鎖定、設定密碼\n[加入]新版本設定介面\n[加入]設定存檔",
            "ver 3.0.2333.38β":"[加入]工作列圖示\n[更新]加入經典、塗鴉主題\n[更新]CLI可跟隨主題\n[加入]自動鎖定、設定密碼\n[加入]新版本設定介面\n[加入]各種神出鬼沒的bug(誤",
            "ver 2.7.1919.810":"[加入]桌布切換\n[加入]主畫面桌布\n[更改]開始選單的間距",
            "ver 2.5.1616.69":"[加入]鎖定畫面\n[加入]更新日誌\n[修復]關機視窗無法選中問題\n[更新]更多的終端機指令",
            "ver 2.0.114.514":"[更改]ShellyOS主介面大幅度更改，修改視窗樣式\n[更新]關於樣式更改\n[移除]刪除瀏覽器\n[更新]文件管理加入資源回收、電腦\n[加入]更完善的關機選單\n[加入]終端機",
            "ver 1.0.114.514":"[開端]ShellyOS的初版本\n[加入]關於\n[加入]瀏覽器\n[加入]記事本\n[加入]文件管理\n[加入]計算器\n"
        }
        
        log("[UpdateLog]App bar button packed")
        
        self.window = Toplevel(master)
        self.window.title("update")
        self.window.geometry("400x300+100+100")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        log("[UpdateLog]Toplevel created")
        
        self.x_offset = 0
        self.y_offset = 0
        
        self.title_bar = Frame(self.window, bg="#eeffff", relief="raised", bd=0)
        self.title_bar.pack(fill="x")
        
        self.title_label = Label(self.title_bar, text="ShellyOS 更新日誌", bg="#eeffff", fg="black", font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        self.exit_btn = Button(self.title_bar, text="✕", command=self.exiting)
        self.exit_btn.pack(side="right")
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.change_color()
        
        log("[UpdateLog]Title bar packed")
        
        Label(self.window,text="ShellyOS 更新日誌", font=("微軟正黑體", 18)).pack(pady=5)
        
        self.action_var = StringVar()
        self.combo = ttk.Combobox(self.window, textvariable=self.action_var, state="readonly")
        self.combo['values'] = ("ver 3.0.2333.38","ver 3.0.2333.38β","ver 2.7.1919.810","ver 2.5.1616.69", "ver 2.0.114.514", "ver 1.0.114.514")
        self.combo.current(0)  # 預設選第一個
        self.combo.pack(pady=5)
        
        self.logs_text = Label(self.window,text="", font=("微軟正黑體", 12), anchor='w')
        self.logs_text.pack()
        
        self.window.after(100,self.change_logs)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.change_logs())

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y
    
    def change_color(self):
        self.btn.config(bg=bgc,fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc,fg=fgc)
    
    def change_logs(self):
        version = self.action_var.get()
        log_text = self.logs.get(version, "找不到更新日誌")
        self.logs_text.config(text=log_text)


    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")
    
    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()
    
    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        apps_running.pop(self.myidx)
        log("[UpdateLog]Got exiting message, destroyed and poped")
    
class FileManager():
    def __init__(self, master, path="S:Computer"):
        self.myidx = len(apps_running)
        self.master = master
        self.path = path
        self.recycle_log = "X:\\bin\\recycle_status.txt"
        self.noremove = ["bin", "Documents"]
        self.protected = ["recycle", "calc.pyw", "files.pyw", "note.pyw", "ungoogled", "recycle", "Windows", "Users", "Program Files", "Program Files (x86)", "ProgramData", "$RECYCLE.BIN", "System Volume Information"]
        
        log("[File]Initialized variables")
        
        self.icon = PhotoImage(file=r"X:\bin\icons\fileman.png")
        self.btn = Button(root, anchor='w',bg=bgc,fg=fgc,image=self.icon, command=self.focus_window)
        self.btn.image = self.icon #以防回收
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        log("[File]App bar button packed")
        self.window = Toplevel(master)
        self.window.title("文件管理器")
        self.window.geometry("600x500+100+100")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        log("[File]Toplevel created")

        self.x_offset = 0
        self.y_offset = 0
        
        self.title_bar = Frame(self.window, bg="#eeeeff")
        self.title_bar.pack(fill="x")
        self.title_label = Label(self.title_bar, text="文件管理器", bg="#eeeeff", font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        self.exit_btn = Button(self.title_bar, text="✕", command=self.exiting)
        self.exit_btn.pack(side="right")
        
        self.restore_btn = Button(self.title_bar, text="回復", command=self.restore, state="disabled")
        self.restore_btn.pack(side="right")
        
        self.del_btn = Button(self.title_bar, text="刪除", command=self.remove, state="disabled")
        self.del_btn.pack(side="right")
        self.rename_btn = Button(self.title_bar, text="重新命名", command=self.rename_window, state="disabled")
        self.rename_btn.pack(side="right")
        self.new_btn = Button(self.title_bar, text="新增資料夾", command=self.new_folder_window)
        self.new_btn.pack(side="right")
        self.back_btn = Button(self.title_bar, text="上一頁", command=self.forward)
        self.back_btn.pack(side="right")
        self.refresh_btn = Button(self.title_bar, text="重新整理", command=self.refresh)
        self.refresh_btn.pack(side="right")
        log("[File]Title bar packed")
        for widget in [self.title_bar, self.title_label]:
            widget.bind("<ButtonPress-1>", self.start_move)
            widget.bind("<B1-Motion>", self.do_move)
        
        self.change_color()
        self.path_label = Label(self.window, text=self.path, font=("微軟正黑體", 10))
        self.path_label.pack()
        
        self.listbox = Listbox(self.window, selectmode="browse", height=20, width=80, font=("微軟正黑體", 12))
        self.listbox.pack(pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<Double-Button-1>", self.open_file_or_dir)
        log("[File]Path label and listbox packed")
        self.nf_wind = None
        self.refresh(isComputer=True)
        self.window.protocol("WM_DELETE_WINDOW", disable_close)

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")

    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    def refresh(self, isComputer=False):
        self.listbox.delete(0, END)
        log("[File]Got refresh command")
        if self.path != "X:\\" and self.path != "S:Computer":
            self.new_btn.config(state="normal")
            self.back_btn.config(state="normal")
            log("[File]It is normal folder, made New and Back enable")
        elif self.path == "X:\\":
            self.new_btn.config(state="disabled")
            self.back_btn.config(state="normal")
            log("[File]It is X disk, made New disable and Back enable")
        else:
            self.new_btn.config(state="disabled")
            self.back_btn.config(state="disabled")
            log("[File]It is root(computer), made New and Back disable")

        if isComputer:
            self.path_label.config(text="電腦")
            self.listbox.insert(END, "本機磁碟機[0]")
            self.listbox.insert(END, "資源回收")
            log("[File]It is root(computer), inserted disk and recycle")
        else:
            os.chdir(self.path)
            if self.path == "X:\\recycle\\":
                self.path_label.config(text="資源回收")
                log("[File]It is recycle, path label changed to recycle")
            dircon = os.listdir()
            self.path_label.config(text="電腦\\本機磁碟機[0]" + self.path[2:])
            for i in dircon:
                if i in self.protected:
                    log(f"[File]Skipped hid dir {i}")
                    continue
                self.listbox.insert(END, i)
                log(f"[File]Inserted tree or file {i}")
            if len(dircon) == 0:
                self.listbox.insert(END, "*此資料夾為空*")
                log("[File]Inserted empty folder message")

    def forward(self):
        if self.path in ["X:\\", "S:Computer","X:\\recycle\\"]:
            self.path = "S:Computer"
            self.refresh(isComputer=True)
            log(f"[File]Got forward command and changed to S:Computer")
        else:
            os.chdir("..")
            self.path = os.getcwd()
            log("[File]Got forward command,changed to {self.path}")
            self.refresh()

    def on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        selected_name = self.listbox.get(selection[0])
        state = "normal" if selected_name not in self.protected else "disabled"
        self.rename_btn.config(state=state)
        self.del_btn.config(state=state)
        self.restore_btn.config(state="normal" if self.path == "X:\\recycle\\" else "disabled")
        log("[File]Got on select command and successed")
        
    def open_file_or_dir(self, event):
        log(f"[File]Got open file or dir command")
        selection = self.listbox.curselection()
        if not selection:
            return
        this_name = self.listbox.get(selection[0])
        full_path = os.path.join(self.path, this_name)
        if os.path.isdir(full_path):
            self.path = full_path
            self.refresh()
            log(f"[File]Went to {this_name}")
        elif this_name == "本機磁碟機[0]":
            self.path = "X:\\"
            self.refresh()
            log("[File]Went to disk")
        elif this_name == "資源回收":
            self.path = "X:\\recycle\\"
            log("[File]Went to recycle")  
            self.refresh()
        elif this_name.endswith(".txt"):
            apps_running.append(Note(self.master, filepath=full_path))
            log("[File]Sent selected file to Note")
        elif this_name == "*此資料夾為空*":
            return
        else:
            MsgBox.info(self.window,"錯誤", "目前無法打開此類型文件")
            log("[File]Returned cannot open this type message")

    def new_folder_window(self):
        log(f"[File]Got new folder window command and trying create toplevel")
        self.nf_wind = Toplevel(self.window)
        self.nf_wind.title("新增資料夾")
        self.nf_wind.geometry("200x100")
        self.nf_wind.attributes("-topmost", True)
        log(f"[File]New folder toplevel created")
        Label(self.nf_wind, text="請輸入資料夾名稱：", font=("微軟正黑體", 12)).pack(pady=5)
        entry = Entry(self.nf_wind)
        entry.pack(pady=5)
        Button(self.nf_wind, text="完成", command=lambda: self.new_folder(entry.get())).pack(pady=5)
        log(f"[File]Packed all about new folder toplevel")
    def new_folder(self, fn):
        try:
            if fn in self.protected or fn in self.noremove:
                MsgBox.error(self.window,"錯誤", "此名稱已被禁止。")
                return
            os.mkdir(os.path.join(self.path, fn or "新增資料夾"))
            self.refresh()
            log(f"[File]New folder created")
        except Exception as e:
            MsgBox.error(self.window,"錯誤", f"無法建立資料夾：{e}")
            log(f"[File]New folder cannot create:{e}")
        finally:
            self.nf_wind.destroy()
            self.nf_wind = None
            log(f"[File]New folder window destroyed")
    
    def rename_window(self):
        log(f"[File]Got rename window command and trying create toplevel")
        self.nf_wind = Toplevel(self.window)
        self.nf_wind.title("重新命名")
        self.nf_wind.geometry("200x100")
        self.nf_wind.attributes("-topmost", True)
        log(f"[File]Rename toplevel created")
        Label(self.nf_wind, text="請輸入新的名稱：", font=("微軟正黑體", 12)).pack(pady=5)
        entry = Entry(self.nf_wind)
        entry.pack(pady=5)
        Button(self.nf_wind, text="完成", command=lambda: self.rename(entry.get())).pack(pady=5)
        log(f"[File]Packed all about rename toplevel")
    def rename(self, fn):
        selection = self.listbox.curselection()
        if not selection:
            return
        selected_name = self.listbox.get(selection[0])
        if fn in self.protected or selected_name in self.protected or fn in self.protected or selected_name in self.noremove:
            MsgBox.error(self.window,"錯誤", "禁止命名為此名稱")
            log(f"[File]Prevented rename to not allowed name")
            return
        os.rename(os.path.join(self.path, selected_name), os.path.join(self.path, fn))
        self.refresh()
        log(f"[File]File renamed")
        self.nf_wind.destroy()
        self.nf_wind = None
        log(f"[File]File window destroyed")

    def remove(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        selected_name = self.listbox.get(selection[0])
        if selected_name in self.protected or selected_name in self.noremove:
            log(f"[File]Prevented remove to not allowed file")
            MsgBox.error(self.window,"錯誤", "禁止刪除或回收此項目")
            return
        full_path = os.path.join(self.path, selected_name)
        
        if self.path == "X:\\recycle\\":
            if MsgBox.ask(self.window,"刪除", "是否永久刪除此項目？"):
                try:
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                    self._remove_log_entry(selected_name)
                    self.refresh()
                except Exception as e:
                    MsgBox.error(self.window,"錯誤", f"刪除失敗：{e}")
                    log(f"[File]Deletefailed:{e}")
        else:
            try:
                shutil.move(full_path, "X:\\recycle\\")
                with open(self.recycle_log, "a", encoding="utf-8") as f:
                    f.write(f"{selected_name},{full_path}\n")
                self.refresh()
                log(f"[File]Recycled {full_path}")
            except Exception as e:
                MsgBox.error(self.window,"錯誤", f"刪除失敗：{e}")
                log(f"[File]Recycle failed:{e}")
                

    def restore(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        selected_name = self.listbox.get(selection[0])
        full_path = os.path.join("X:\\recycle\\", selected_name)
        
        try:
            with open(self.recycle_log, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            restored = False
            for line in lines:
                name, orig = line.strip().split(",", 1)
                if name == selected_name:
                    shutil.move(full_path, orig)
                    restored = True
                else:
                    new_lines.append(line)
            if restored:
                with open(self.recycle_log, "w", encoding="utf-8") as f:
                    f.writelines(new_lines)
                self.refresh()
                log(f"[File]Restored file")
            else:
                MsgBox.error(self.window,"錯誤", "找不到原始路徑，無法回復")
                log(f"[File]Restore failed:{e}")
        except Exception as e:
            MsgBox.error(self.window,"錯誤", f"回復失敗：{e}")
            log(f"[File]Restore failed:{e}")

    def _remove_log_entry(self, filename):
        try:
            with open(self.recycle_log, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(self.recycle_log, "w", encoding="utf-8") as f:
                for line in lines:
                    if not line.startswith(filename + ","):
                        f.write(line)
            log(f"[File]Recycle log added")
        except:
            pass

    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        apps_running.pop(self.myidx)
        log(f"[File]Got exiting message, destroyed and poped")
        
    def change_color(self):
        self.btn.config(bg=bgc,fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc,fg=fgc)

class Settings():
    def __init__(self, master):
        global theme
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.icon = PhotoImage(file=r"X:\bin\icons\setting.png")
        self.btn = Button(root, anchor='w', bg=bgc, fg=fgc, image=self.icon, command=self.focus_window)
        self.btn.image = self.icon
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        log("[Settings]App bar button packed")
        
        self.window = Toplevel(master)
        self.window.title("Settings")
        self.window.geometry("335x125+100+100")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        log("[Settings]Toplevel created")
        
        self.x_offset = 0
        self.y_offset = 0
        
        self.title_bar = Frame(self.window, bg="#eeffff", relief="raised", bd=0)
        self.title_bar.pack(fill="x")
        
        self.title_label = Label(self.title_bar, text="設定", bg="#eeffff", fg="black", font=("微軟正黑體", 12))
        self.title_label.pack(side="left", padx=5)
        
        self.exit_btn = Button(self.title_bar, text="✕", command=self.exiting)
        self.exit_btn.pack(side="right")
        log("[Settings]Title bar packed")
        
        self.frame = Frame(self.window)
        self.frame.pack(fill="both", expand=True)
        
        Label(self.frame, text="自動鎖定(分鐘)：", width=15,anchor="e", font=("微軟正黑體", 10)).grid(column=0,row=0, sticky="e",pady=3)
        self.vcmd = (self.frame.register(self.is_int), "%P")
        self.locktime_entry = Entry(self.frame, validate="key",width=23, validatecommand=self.vcmd)
        self.locktime_entry.insert(0,auto_lock_time)
        self.locktime_entry.grid(column=1,row=0,padx=3,pady=3)
        self.apply_lock_btn = Button(self.frame, text="套用", command=self.apply_locktime)
        self.apply_lock_btn.grid(column=2,row=0, sticky="e",pady=3)
        
        Label(self.frame, text="設定密碼：", width=15, anchor="e", font=("微軟正黑體", 10)).grid(column=0,row=1, sticky="e",pady=3)
        self.password_entry = Entry(self.frame, show="*", font=("微軟正黑體", 10),width=20)
        self.password_entry.grid(column=1,row=1,pady=3,padx=3)
        self.apply_pass_btn = Button(self.frame, text="套用", command=self.save_password)
        self.apply_pass_btn.grid(column=2,row=1, sticky="e",pady=3)
        
        Label(self.frame, text="設定主題：", width=15,anchor="e", font=("微軟正黑體", 10)).grid(column=0,row=2, sticky="e",pady=3)
        self.action_var = StringVar()
        self.combo = ttk.Combobox(self.frame, textvariable=self.action_var, state="readonly")
        self.combo['values'] = ("預設", "城市夜晚", "海面", "經典", "塗鴉")
        self.combo.current(["default","night","sea","basic","doodle"].index(theme))
        self.combo.grid(column=1,row=2,padx=3,pady=3)
        
        self.apply_theme_btn = Button(self.frame, text="套用", command=self.apply_theme)
        self.apply_theme_btn.grid(column=2,row=2, sticky="e",pady=3)
        
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        self.change_color()
        self.window.protocol("WM_DELETE_WINDOW", disable_close)

    def is_int(self, value):
        if value == "":
            return True
        try:
            val = int(value)
            return 0 <= val <= 300
        except:
            return False
    
    
    
    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")

    def change_color(self):
        self.btn.config(bg=bgc, fg=fgc)
        self.title_bar.config(bg=bgc)
        self.title_label.config(bg=bgc, fg=fgc)

    def focus_window(self):
        self.window.deiconify()
        self.window.lift()
        self.window.focus_force()

    def exiting(self):
        self.btn.destroy()
        if self.btn in appbar_apps:
            appbar_apps.remove(self.btn)
        self.window.destroy()
        apps_running.pop(self.myidx)
        log("[Settings]Got exiting message, destroyed and poped")

            
    def apply_locktime(self):
        try:
            locktime = int(self.locktime_entry.get())
            config["auto_lock_time"] = locktime
            save_config()
            global auto_lock_time
            auto_lock_time = locktime
            log(f"[Settings]Auto lock time set to {locktime} seconds")
        except Exception as e:
            MsgBox.error(self.window, "錯誤", f"時間儲存失敗：{e}")
            log(f"[Settings]Error saving lock time: {e}")
    
    def save_password(self):
        global saved_hash
        password = self.password_entry.get()
        hashed = hashlib.sha256(password.encode("utf-8")).hexdigest() if password else ""
        try:
            config["password_hash"] = hashed
            save_config()
            saved_hash = hashed
            log("[Settings]Password saved and hash updated")
        except Exception as e:
            MsgBox.error(self.window, "錯誤", f"儲存失敗：{e}")
            log(f"[Settings]Error saving password: {e}")
            
    def apply_theme(self):
        global theme
        theme_name = {
            "預設": "default",
            "城市夜晚": "night",
            "海面": "sea",
            "經典": "basic",
            "塗鴉": "doodle"
        }
        theme = theme_name[self.action_var.get()]
        config["theme"] = theme
        save_config()
        change_theme(theme)


def log(e):
    print(e)

def timeset():
    global locking, timer
    now = datetime.datetime.now()
    fot = now.strftime("%y/%m/%d (%a) %H:%M:%S")
    timelabel.config(text=fot)
    if locking == False:
        timer += 0.1
    if timer >= float(auto_lock_time) * 60:
        LockScreen(root)
    root.after(100, timeset)

def change_theme(t):
    global lock_wall, backg_label, pc_shortcut, pc_shortlab, bgc, fgc, menu_btn
    path = "X:\\bin\\wallpaper\\"
    walls = {
        "example": ["wallpaper.png", "lock.png", "icon_color","taskbar","button","font"],
        "default": ["default1.png", "default2.png", "#627C36","#7FAD8E","#7EA568","#fff"],
        "night": ["night1.png", "night2.png", "#C9B0A9","#222","#333","#fff"],
        "sea": ["water.png", "water.png", "#378AC9","#1466A2","#398FCF","#BCD9EE"],
        "basic": ["basic.png", "basic.png", "#028381","#F0F0F0","#F0F0F0","#000"],
        "doodle": ["doodle1.png", "doodle2.png", "#fff","#272","#4a4","#fff"]
    }
    
    
    # 更新桌布
    backg_img_path = os.path.join(path, walls[t][0])
    new_img = PhotoImage(file=backg_img_path)
    backg_label.config(image=new_img)
    backg_label.image = new_img  # 防止被回收

    # 更新鎖定畫面路徑
    lock_wall = os.path.join(path, walls[t][1])

    # 更新圖示背景色
    pc_shortcut.config(bg=walls[t][2])
    pc_shortlab.config(bg=walls[t][2])
    
    root.configure(background=walls[t][3])
    bgc = walls[t][4]
    fgc = walls[t][5]
    timelabel.config(bg=walls[t][3],fg=fgc)
    menu_btn.config(bg=bgc,fg=fgc)
    
    for i in apps_running:
        i.change_color()

def save_config():
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
 
def runapp(e):
    start_destroy()
    if e == "note":
        apps_running.append(Note(root))
        log(f"[Start]Got {e},Called Note")
    elif e == "about":
        apps_running.append(About(root))
        log(f"[Start]Got {e},Called About")
    elif e == "calc":
        apps_running.append(Calc(root))
        log(f"[Start]Got {e},Called Calc")
    elif e == "shutdown":
        apps_running.append(SafeShutdown(root))
        log(f"[Start]Got {e},Called Shutdown")
    elif e == "terminal":
        apps_running.append(CommandLine(root))
        log(f"[Start]Got {e},Called Command Line")
    elif e == "updatelog":
        apps_running.append(UpdateLog(root))
        log(f"[Start]Got {e},Called Update Log")
    elif e == "file":
        apps_running.append(FileManager(root))
        log(f"[Start]Got {e},Called File Manager")
    elif e == "settings":
        apps_running.append(Settings(root))
        log(f"[Start]Got {e},Called Theme Changer")

def run_start():
    global start_open, start
    
    apps = [
        ["記事本", "note"], 
        ["文件管理器", "file"], 
        ["計算機", "calc"], 
        ["關於", "about"], 
        ["終端機", "terminal"],
        ["更新日誌","updatelog"],
        ["設定","settings"],
        ["關閉 / 登出", "shutdown"]
    ]
    
    start_open = True
    start = Toplevel(root)
    start.attributes("-topmost", True)
    start.title("start")
    start.geometry("150x"+str(35*len(apps))+"+0+"+str(768-35*len(apps)-30))
    start.overrideredirect(True)
    start.bind("<FocusOut>", lambda e: start_destroy())
    log(f"[Start]Toplevel created")

    for app in apps:
        Button(start, text=app[0], font=("微軟正黑體", 12), height=1, width=20,fg=fgc,bg=bgc, anchor='w',
               command=lambda x=app[1]: runapp(x)).pack(side='top')
    log(f"[Start]Buttons packed")

def start_destroy():
    global start_open, start
    if start:
        start.destroy()
    start_open = False
    start = None
    log(f"[Start]Destroyed")

def startmenu():
    global start_open
    if start_open is False:
        run_start()
    else:
        start_destroy()
    log(f"[Taskbar]Toggled start")

def reset_timer(event="是的又是我佔位符"):
    global timer
    timer = 0

def disable_close():
    pass  # 不做任何事，或顯示警告視窗

def initialization():
    global log_file, timer, root, appbar_apps, apps_running, shutdown_bg, shutdown_window, start, start_open, config_file
    global bg, timelabel, backg_label, pc_shortcut, pc_shortlab, menu_btn, saved_hash, locking, auto_lock_time, theme, config
    root = Tk()
    root.title("taskbar")
    root.geometry("1024x30+0+738")
    root.configure(background='#222')
    root.overrideredirect(True)
    
    log(f"[Init]Root created")

    appbar_apps = []
    apps_running = []
    shutdown_bg = None
    shutdown_window = None    
    start = None
    start_open = False
    
    log(f"[Init]Variables initialized")
    
    bg = Toplevel(root)
    bg.title("desktop")
    bg.geometry("1024x768")
    bg.configure(background='#0078D4')
    bg.overrideredirect(True)
    
    backg_image = PhotoImage(file=r"X:\bin\wallpaper\default1.png")
    backg_label = Label(bg, image=backg_image, bg='#0078D4')
    backg_label.image = backg_image  # 防止被回收
    backg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    log(f"[Init]Background toplevel created")
    
    pc_icon = PhotoImage(file="X:/bin/icons/pc.png")
    
    pc_shortcut = Label(bg, image=pc_icon, bg='#627C36')
    pc_shortcut.image = pc_icon  # 防止被回收
    pc_shortcut.place(x=50, y=50)
    pc_shortcut.bind("<Button-1>", lambda x="這是佔位符":apps_running.append(FileManager(root)))
    #lambda x="S:Computer":apps_running.append(FileManager(root,x))
    
    pc_shortlab = Label(bg,text="電腦",font=("微軟正黑體", 11),bg='#627C36')
    pc_shortlab.place(x=68, y=117)
    
    log(f"[Init]Computer shortcut created")
    
    menu_btn = Button(root, text="選單", font=("微軟正黑體", 12),bg=bgc,fg=fgc, command=startmenu)
    menu_btn.pack(side='left')
    timelabel = Label(root, text="00:00",bg="#222",fg="#fff", font=("微軟正黑體", 12))
    timelabel.pack(side='right')
    
    log(f"[Init]Menu and time label packed") 
    log(f"[Init]Initialized, welcome to ShellyOS!")  
    locking = False
    timer = 0.0
    
    saved_hash = ""
    config_file = "X:/bin/config.json"

    # 預設設定
    default_config = {
        "password_hash": "",
        "auto_lock_time": 5,
        "theme": "default"
    }

    # 讀取或建立設定檔
    if os.path.isfile(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            log(f"[Init]Config read failed: {e}")
            config = default_config
    else:
        config = default_config
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

    # 套用設定
    saved_hash = config["password_hash"]
    auto_lock_time = config["auto_lock_time"]
    theme = config["theme"]
    change_theme(theme)
    
    root.after(100, timeset)
    root.after(1, LockScreen, root)
    root.protocol("WM_DELETE_WINDOW", disable_close)
    bg.protocol("WM_DELETE_WINDOW", lambda x="這是佔位符": apps_running.append(SafeShutdown(root)))
    
    root.bind_all("<Motion>", reset_timer)      # 滑鼠移動
    root.bind_all("<Key>", reset_timer)         # 按下任何鍵
    root.bind_all("<Button>", reset_timer)      # 滑鼠點擊

    
    root.mainloop()
root = None
pc_icon = None
recycle_icon = None
appbar_apps = []
apps_running = []
shutdown_window = None
start = None
start_open = False
bg = None
timelabel = None
pc_labe = None
recycle_label = None
lock_wall = ""
bgc = "#333"
fgc = "#fff"

initialization()
