from tkinter import *
from sys import argv

root = Tk()
root.geometry("1024x768")
root.configure(background='#aa2222')
root.overrideredirect(True)
root.attributes("-topmost", True)
root.config(cursor="none")

try:
    error_code = argv[1]
except:
    error_code = "FOR_TEST_NOW"
def ret():pass

Label(root,text="This computer has been crashed and need to restart.",font=("微軟正黑體", 20),bg='#aa2222',fg="#ffffff").place(relx=0.5, rely=0.5, anchor="center")
root.protocol("WM_DELETE_WINDOW", ret)

Label(root,text=f"STOP CODE = {error_code}",font=("微軟正黑體", 12),bg='#aa2222',fg="#ffffff").place(relx=0.5, rely=1,anchor="s")

root.mainloop()
