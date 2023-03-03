import tkinter as tk
from frames import load_f1


root = tk.Tk()

# SETUP
root.title("Timetabling")

# centrul ecranului
#root.eval("tk::PlaceWindow . center")
x = root.winfo_screenwidth() // 3
y = int(root.winfo_screenheight() * 0.1)
root.geometry('600x700+' + str(x) + '+' + str(y))
root.minsize(600, 700)
root.maxsize(600, 700)

f1 = tk.Frame(root, width=600, height=700, bg="#2e525b")
f2 = tk.Frame(root, width=600, height=700, bg="#2e525b")
f3 = tk.Frame(root, width=600, height=700, bg="#2e525b")

for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky="nesw")

load_f1(f1, f2, f3, False)

input_username = tk.StringVar()

root.mainloop()
