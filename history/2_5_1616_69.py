from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from subprocess import Popen as popen
import shutil
import datetime
import os
import time

class LockScreen():
    def __init__(self, master):
        self.master = master
        root.attributes("-topmost", False)
        
        self.window = Toplevel(root)
        self.window.title("ShellyOS Lock Screen")
        self.window.geometry("1024x768")
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(background='#0078D4')
        log("[LockScreen]Toplevel created")
        # 載入 PNG 或 GIF 圖片
        self.bg_image = PhotoImage(file=r"X:\bin\wallpaper\lock.png")

        # 設定 Label 為背景
        self.bg_label = Label(self.window, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        log("[LockScreen]Background applyed")
        self.time_label = Label(self.window,text="00:00",font=("微軟正黑體",30),bg="#444",fg="#fff")
        self.time_label.pack(fill="x",side='top')
        self.date_label = Label(self.window, text="2000/01/01 (Sat)", font=("微軟正黑體", 16), bg="#444", fg="#ddd")
        self.date_label.pack(fill="x")
        log("[LockScreen]Time / date label packed")
        self.window.after(100, self.time_set)

        Button(self.window,text="解鎖",font=("微軟正黑體",20),command=self.unlock,bg="#444",fg="#fff").pack(fill="x",side='bottom')
        
        log("[LockScreen]Unlock button packed")
        self.window.protocol("WM_DELETE_WINDOW", disable_close)
        
    def unlock(self):
        self.window.destroy()
        root.attributes("-topmost", True)
        log("[LockScreen]Got unlock message, destroyed")
    def time_set(self):
        now = datetime.datetime.now()
        fod = now.strftime("%Y/%m/%d (%a)")
        self.date_label.config(text=fod)
        fot = now.strftime("%H:%M")
        self.time_label.config(text=fot)
        self.window.after(1000, self.time_set)

class About():
    def __init__(self, master):
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.btn = Button(root, text="關於 ShellyOS", font=("微軟正黑體", 12), anchor='w',bg="#333",fg="#fff", width=15, command=self.focus_about)
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
        
        Label(self.window,text="關於 ShellyOS", font=("微軟正黑體", 18)).pack(pady=5)
        Label(self.window,text="ShellyOS v.2.5.1616.69\n未經授權可以轉載\n\n基於Windows 11 PE與Pyinstaller\n\nWindows、Windows PE和Aero Basic是\nMicrosoft Corp.的註冊商標", font=("微軟正黑體", 12)).pack(pady=5)
        log("[About]Contect labels packed")
        if os.path.isfile('C:\\Windows\\explorer.exe'):
            Label(self.window,text="目前正在測試", font=("微軟正黑體", 10)).pack(pady=5)
            log("[About]For test label packed")
        
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
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
    
    def focus_about(self):
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
    
    
class Calc():
    def __init__(self, master):
        self.myidx = len(apps_running)-1
        self.master = master
        
        self.btn = Button(root, text="計算機", font=("微軟正黑體", 12),bg="#333",fg="#fff", anchor='w', width=15, command=self.focus_window)
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        log("[Calc]App bar button packed")
        
        self.window = Toplevel(root)
        self.window.title("計算機")
        self.window.geometry("343x520")
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
        
        self.exit_btn = Button(self.title_bar, text="離開", command=self.exiting)
        self.exit_btn.pack(side="right", padx=2)
        log("[Calc]Title bar packed")
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        
        self.content_frame = Frame(self.window)
        self.content_frame.pack(fill="both", expand=True)
        
        self.entry = Entry(self.content_frame, font=("微軟正黑體", 20), justify="right")
        self.entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="we")
        log("[Calc]Entry packed")
        self.buttons = [
            ("+", 1, 0), ("-", 1, 1), ("*", 1, 2),
            ("/", 2, 0), ("CE", 2, 1), ("x²", 2, 2),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2),
            ("0", 6, 0), ("C", 6, 1), ("=", 6, 2),
        ]
        
        

        for (text, row, col) in self.buttons:
            if text == "C":
                cmd = self.clear
            elif text == "=":
                cmd = self.calculate
            elif text == "CE":
                cmd = self.clslast
            else:
                cmd = lambda x=text: self.press(x)
            Button(self.content_frame, text=text, font=("微軟正黑體", 16), width=3, height=2, command=cmd).grid(row=row, column=col, sticky="nsew")
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
        self.btn = Button(root, text="記事本", font=("微軟正黑體", 12), anchor='w',bg="#333",fg="#fff", width=15, command=self.focus_note)
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
        Button(self.title_bar, text="離開", command=self.exiting).pack(side="right", padx=2)
        Button(self.title_bar, text="檔案", command=self.show_file_menu).pack(side="right", padx=2)
        log("[Note]Title bar packed")
        # 綁定拖曳事件
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)

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
    def focus_note(self):
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
        
        self.btn = Button(root, text="ShellyOS 指令", font=("微軟正黑體", 12),bg="#333",fg="#fff", anchor='w', width=15, command=self.focus_window)
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
        
        self.exit_btn = Button(self.title_bar, text="離開", command=self.exiting)
        self.exit_btn.pack(side="right", padx=2)
        log("[Command]Title bar created")
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        
        self.text_area = Text(self.window, font=("微軟正黑體", 12))
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<Return>", self.execute_command)
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
            "ver": lambda command: self.text_area.insert(END, "\nShellyOS Terminal v.2.5.1616.69 未經授權可以轉載"),
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
            safe_shutdown()
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
        
        self.btn = Button(root, text="ShellyOS 更新日誌", font=("微軟正黑體", 12), anchor='w',bg="#333",fg="#fff", width=15, command=self.focus_about)
        self.btn.pack(side='left')
        appbar_apps.append(self.btn)
        
        self.logs = {
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
        
        self.exit_btn = Button(self.title_bar, text="離開", command=self.exiting)
        self.exit_btn.pack(side="right", padx=5)
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<ButtonPress-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)
        
        log("[UpdateLog]Title bar packed")
        
        Label(self.window,text="ShellyOS 更新日誌", font=("微軟正黑體", 18)).pack(pady=5)
        
        self.action_var = StringVar()
        self.combo = ttk.Combobox(self.window, textvariable=self.action_var, state="readonly")
        self.combo['values'] = ("ver 2.5.1616.69", "ver 2.0.114.514", "ver 1.0.114.514")
        self.combo.current(0)  # 預設選第一個
        self.combo.pack(pady=5)
        
        self.logs_text = Label(self.window,text="", font=("微軟正黑體", 12), anchor='w')
        self.logs_text.pack()
        
        self.window.after(100,self.change_logs)
        self.combo.bind("<<ComboboxSelected>>", lambda e: self.change_logs())

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y
    
    def change_logs(self):
        version = self.action_var.get()
        log_text = self.logs.get(version, "找不到更新日誌")
        self.logs_text.config(text=log_text)


    def do_move(self, event):
        x = self.window.winfo_pointerx() - self.x_offset
        y = self.window.winfo_pointery() - self.y_offset
        self.window.geometry(f"+{x}+{y}")
    
    def focus_about(self):
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
        self.protected = ["bin", "Documents", "recycle", "calc.pyw", "files.pyw", "note.pyw", "ungoogled"]
        
        log("[File]Initialized variables")
        
        self.btn = Button(root, text="文件管理器", font=("微軟正黑體", 12), anchor='w', width=15, bg="#333", fg="#fff", command=self.focus_window)
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
        
        self.restore_btn = Button(self.title_bar, text="回復", command=self.restore, state="disabled")
        self.restore_btn.pack(side="right")
        self.exit_btn = Button(self.title_bar, text="離開", command=self.exiting)
        self.exit_btn.pack(side="right", padx=5)

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
                if i in ["recycle", "Windows", "Users", "Program Files", "Program Files (x86)", "ProgramData", "$RECYCLE.BIN", "System Volume Information"]:
                    continue
                    log(f"[File]Skipped hid dir {i}")
                self.listbox.insert(END, i)
                log(f"[File]Inserted tree or file {i}")
            if len(dircon) == 0:
                self.listbox.insert(END, "*此資料夾為空*")
                log("[File]Inserted empty folder message")

    def forward(self):
        if self.path in ["X:\\", "S:Computer"]:
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
            messagebox.showinfo("錯誤", "目前無法打開此類型文件")
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
            os.mkdir(os.path.join(self.path, fn or "新增資料夾"))
            self.refresh()
            log(f"[File]New folder created")
        except Exception as e:
            messagebox.showerror("錯誤", f"無法建立資料夾：{e}")
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
        if fn in self.protected or selected_name in self.protected:
            messagebox.showerror("錯誤", "禁止命名為此名稱")
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
        if selected_name in self.protected:
            log(f"[File]Prevented remove to not allowed file")
            messagebox.showerror("錯誤", "禁止刪除或回收此項目")
            return
        full_path = os.path.join(self.path, selected_name)
        
        if self.path == "X:\\recycle\\":
            if messagebox.askyesno("刪除", "是否永久刪除此項目？"):
                try:
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                    elif os.path.isdir(full_path):
                        shutil.rmtree(full_path)
                    self._remove_log_entry(selected_name)
                    self.refresh()
                except Exception as e:
                    messagebox.showerror("錯誤", f"刪除失敗：{e}")
                    log(f"[File]Deletefailed:{e}")
        else:
            try:
                shutil.move(full_path, "X:\\recycle\\")
                with open(self.recycle_log, "a", encoding="utf-8") as f:
                    f.write(f"{selected_name},{full_path}\n")
                self.refresh()
                log(f"[File]Recycled {full_path}")
            except Exception as e:
                messagebox.showerror("錯誤", f"刪除失敗：{e}")
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
                messagebox.showerror("錯誤", "找不到原始路徑，無法回復")
                log(f"[File]Restore failed:{e}")
        except Exception as e:
            messagebox.showerror("錯誤", f"回復失敗：{e}")
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

def log(e):
    print(e)
    

def timeset():
    now = datetime.datetime.now()
    fot = now.strftime("%y/%m/%d (%a) %H:%M:%S")
    timelabel.config(text=fot)
    root.after(100, timeset)


def safe_shutdown():
    global shutdown_window
        
    shutdown_window = Toplevel(root)
    shutdown_window.title("shutdownbg")
    shutdown_window.geometry("300x200+362+284")
    shutdown_window.overrideredirect(True)
    shutdown_window.attributes("-topmost", True)
    log(f"[Shutdown]Toplevel created")
    
    def exit_shutdown():
        shutdown_window.destroy()
        log(f"[Shutdown]Canceled, destroyed self")
    
    def execute_action():
        action = action_var.get()
        if action == "關機":
            for i in apps_running:
                idx = app_running.index(o)
                i.exiting()
                log(f"[Shutdown]Notice app {i} ({idx})exiting")
            shutdown_window.destroy() 
            log(f"[Shutdown]Destroyed self")            
            bg.destroy()
            log(f"[Shutdown]Destroyed background")
            root.destroy()
            log(f"[Shutdown]Destroyed root and trying shutdown")

            popen("wpeutil shutdown")
        elif action == "重新啟動":
            try:
                for i in apps_running:
                    i.exiting()
                    log(f"[Shutdown]Notice app {i} ({idx})exiting")
                shutdown_window.destroy()  
                log(f"[Shutdown]Destroyed self")   
                bg.destroy()
                log(f"[Shutdown]Destroyed background")
                root.destroy()
                log(f"[Shutdown]Destroyed root and trying shutdown")

                popen("wpeutil reboot")
            except:
                print(f"[Init]Experiment envitment, will re-initialization after 3 seconds")
                time.sleep(3)
                initialization()
        elif action == "鎖定":
            LockScreen(root)
            shutdown_window.destroy()
            log(f"[Shutdown]Called LockScreen and destroyed self")
        else:
            messagebox.showinfo("提示", "請選擇一個有效的選項")
            log(f"[Shutdown]Unusable chosen, returned")

    # 標題文字
    label = Label(shutdown_window, text="感謝使用ShellyOS!\n請問想讓電腦做甚麼？", font=("Microsoft JhengHei", 12))
    label.pack(pady=10)
    

    # 使用 ttk 的 Combobox 顯示下拉選單
    action_var = StringVar()
    combo = ttk.Combobox(shutdown_window, textvariable=action_var, state="readonly")
    combo['values'] = ("關機", "重新啟動", "鎖定")
    combo.current(0)  # 預設選第一個
    combo.pack(pady=5)
    
    # 確定按鈕
    confirm_button = Button(shutdown_window, text="確定",width=6, height=1, command=execute_action)
    confirm_button.pack(pady=10)
    cancel_button = Button(shutdown_window, text="取消",width=6, height=1, command=exit_shutdown)
    cancel_button.pack(pady=10)
    
    log(f"[Shutdown]Label, combo and buttons packed")


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
        safe_shutdown()
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


def run_start():
    global start_open, start
    
    start_open = True
    start = Toplevel(root)
    start.attributes("-topmost", True)
    start.title("start")
    start.geometry("150x385+0+353")
    start.overrideredirect(True)
    start.bind("<FocusOut>", lambda e: start_destroy())
    log(f"[Start]Toplevel created")
    apps = [
        ["記事本", "note"], 
        ["文件管理器", "file"], 
        ["計算機", "calc"], 
        ["關於", "about"], 
        ["終端機", "terminal"],
        ["更新日誌","updatelog"],
        ["關閉 / 登出", "shutdown"]
    ]
    for app in apps:
        Button(start, text=app[0], font=("微軟正黑體", 12), height=2, width=20, anchor='w',
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

def disable_close():
    pass  # 不做任何事，或顯示警告視窗

def initialization():
    global log_file, root, appbar_apps, apps_running, shutdown_bg, shutdown_window, start, start_open, bg, timelabel
    root = Tk()
    root.title("taskbar")
    root.geometry("1024x30+0+738")
    root.configure(background='#222')
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    
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
    
    
    log(f"[Init]Background toplevel created")
    
    pc_icon = PhotoImage(file="X:/bin/icons/pc.png")
    
    pc_button = Button(bg, image=pc_icon, bg='#0078D4', command=lambda x="S:Computer":apps_running.append(FileManager(root,x)))
    pc_button.image = pc_icon  # 防止被回收
    pc_button.place(x=50, y=50)
    
    Label(bg,text="　電腦",font=("微軟正黑體", 11),bg='#0078D4').place(x=50, y=117)
    
    log(f"[Init]Computer shortcut created")
    
    Button(root, text="選單", font=("微軟正黑體", 12),bg="#333",fg="#fff", command=startmenu).pack(side='left')
    timelabel = Label(root, text="00:00",bg="#222",fg="#fff", font=("微軟正黑體", 12))
    timelabel.pack(side='right')
    log(f"[Init]Menu and time label packed") 
    log(f"[Init]Initialized, welcome to ShellyOS!")    
    root.after(100, timeset)
    root.after(10, LockScreen, root)
    root.protocol("WM_DELETE_WINDOW", disable_close)
    bg.protocol("WM_DELETE_WINDOW", safe_shutdown)
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

initialization()
