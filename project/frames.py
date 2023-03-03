import time
import tkinter as tk
from tkinter import ttk, W, CENTER, NO, Y
from PIL import Image, ImageTk
from functions import clear, add_class, remove_class, operate_classes, fetch_db, save_file, call_algorithm


# form entries with placeholders
class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", font=("TkMenuFont", 13), color='grey', password=False):
        super().__init__(master)

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.placeholder = placeholder
        self.placeholder_font = font
        self.placeholder_color = color
        self.background_color = "#cce1e5"
        self.default_fg_color = self['fg']
        if password:
            self.show = "*"
        else:
            self.show = ""

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, str(self.placeholder))
        self['fg'] = self.placeholder_color
        self['bg'] = "lightgrey"
        self['font'] = self.placeholder_font

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
            self['bg'] = self.background_color
            self['show'] = self.show

    def foc_out(self, *args):
        if not self.get():
            self['show'] = ""
            self.put_placeholder()


def process(user_input, pass_input, com, f1, f2, f3):
    # print("received command " + com + " with input: " + user_input + " and " + pass_input)
    username = ""

    if com == "login":
        username = fetch_db(com, user_input, pass_input)
        # print("rezultat: " + str(username))
    elif com == "create":
        username = fetch_db(com, user_input, pass_input)
        # print("rezultat: " + str(username))

    if username != "":
        load_f2(f1, f2, f3, str(username))
    else:
        load_f1(f1, f2, f3, True)


def load_f1(f1, f2, f3, err):
    clear(f1)
    clear(f2)
    f1.tkraise()

    # f1 nu modifica root
    f1.pack_propagate(False)

    # widgets
    logo = ImageTk.PhotoImage(file="./pictures/logo-01.png")
    logo_widget = tk.Label(f1, image=logo, bg="#2e525b")
    logo_widget.image = logo
    logo_widget.pack()

    tk.Label(f1, text="Generează-ți orarul eficient!", bg="#2e525b", fg="#cce1e5", font=("TkMenuFont", 16)).pack(
        pady=10)

    username = EntryWithPlaceholder(f1, "Nume utilizator", ("TkMenuFont", 14))
    password = EntryWithPlaceholder(f1, "Parola", ("TkMenuFont", 14), 'gray', True)
    username.pack(pady=10)
    password.pack(pady=10)

    error_text = ""
    if err:
        error_text = "Date necorespunzătoare!"

    tk.Label(f1, text=error_text, bg="#2e525b", fg="#cce1e5", font=("TkMenuFont", 14)).pack()

    tk.Button(f1, text="Loghează-te", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13), cursor="hand2",
              activebackground="white", activeforeground="black",
              command=lambda: process(username.get(), password.get(), "login", f1, f2, f3)) \
        .pack(ipady=5, ipadx=5, padx=65, side=tk.LEFT)
    tk.Button(f1, text="Creează cont", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13), cursor="hand2",
              activebackground="white", activeforeground="black",
              command=lambda: process(username.get(), password.get(), "create", f1, f2, f3)) \
        .pack(ipady=5, ipadx=5, padx=65, side=tk.RIGHT)


def load_f2(f1, f2, f3, name):
    clear(f1)
    clear(f3)
    f2.tkraise()

    # f2 nu modifica root
    f2.pack_propagate(False)

    # widgets
    logo = ImageTk.PhotoImage(file="./pictures/logo2-01.png")
    logo_widget = tk.Label(f2, image=logo, bg="#2e525b")
    logo_widget.image = logo
    logo_widget.grid(rowspan=1, column=0, row=0, sticky="w", padx=10)


    greet_label = tk.Label(f2, text="Bună, " + name + "!", bg="#2e525b", fg="#cce1e5", font=("TkHeadingFont", 20))
    greet_label.grid(rowspan=1, column=0, row=0, sticky="e", padx=10)
    instr_label = tk.Label(f2, text="Adaugă toate materiile pe rând și treci mai departe pentru generarea orarului.",
                           bg="#2e525b", fg="#cce1e5", font=("TkMenuFont", 13))
    instr_label.grid(rowspan=1, column=0, row=1, padx=10, pady=5)


    item_name = EntryWithPlaceholder(f2, "Nume materie", ("TkMenuFont", 15))
    item_name.grid(column=0, row=2, padx=10, pady=15)

    DAYS = ["Luni", "Marți", "Miercuri", "Joi", "Vineri"]
    HOURS = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]
    day_variable = tk.StringVar(f2)
    hour_variable = tk.StringVar(f2)
    day_variable.set(DAYS[0])  # valori default
    hour_variable.set(HOURS[0])

    day_select = tk.OptionMenu(f2, day_variable, *DAYS)
    day_select.grid(column=0, row=3, sticky="ew", padx=165)
    hour_select = tk.OptionMenu(f2, hour_variable, *HOURS)
    hour_select.grid(column=0, row=4, sticky="ew", padx=165, pady=5)

    class_listbox = tk.Listbox(f2)
    export_list = []

    add_img = Image.open("./pictures/add-02.png")
    add_img = ImageTk.PhotoImage(add_img)
    pop_img = Image.open("./pictures/pop-03.png")
    pop_img = ImageTk.PhotoImage(pop_img)
    add_button = tk.Button(f2, image=add_img,
                           command=lambda: add_class(class_listbox, item_name.get(), day_variable.get(),
                                                         hour_variable.get(), export_list),
                           width=60, height=60, bg="#2e525b", activebackground="#2e525b", bd=0)
    add_button.image = add_img
    add_button.grid(rowspan=2, column=0, row=3, padx=60, sticky="e")
    pop_button = tk.Button(f2, image=pop_img,
                           command=lambda: remove_class(class_listbox, class_listbox.curselection(), export_list),
                           width=60, height=60, bg="#2e525b", activebackground="#2e525b", bd=0)
    pop_button.image = pop_img
    pop_button.grid(rowspan=2, column=0, row=3, padx=60, sticky="w")

    class_listbox.grid(column=0, row=5, rowspan=2, sticky="ew", padx=165, pady=10, ipady=50)
    scrollbar = tk.Scrollbar(class_listbox)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    class_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=class_listbox.yview)

    back_button = tk.Button(f2, text="Înapoi", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13), cursor="hand2",
                            activebackground="#badee2", activeforeground="black",
                            command=lambda: load_f1(f1, f2, f3, False))
    load_button = tk.Button(f2, text="Încarcă fișier", bg="#2596be", fg="#cce1e5", font=("TkMenuFont", 13), cursor="hand2",
                            activebackground="#badee2", activeforeground="white",
                            command=lambda: operate_classes(f2, class_listbox, export_list))
    next1_button = tk.Button(f2, text="Generează ACO", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13),
                            cursor="hand2", activebackground="#badee2", activeforeground="black",
                            command=lambda: load_f3(f1, f2, f3, export_list, name, True, True, 0, 0))
    next2_button = tk.Button(f2, text="Generează TS", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13),
                             cursor="hand2", activebackground="#badee2", activeforeground="black",
                             command=lambda: load_f3(f1, f2, f3, export_list, name, True, False, 0, 0))

    back_button.grid(rowspan=1, column=0, row=7, sticky="w", padx=30, pady=10)
    next1_button.grid(rowspan=1, column=0, row=7, sticky="e", padx=30, pady=10)
    load_button.grid(rowspan=1, column=0, row=7, sticky="", padx=30, pady=10)
    next2_button.grid(rowspan=1, column=0, row=8, sticky="e", padx=30, pady=10)


def load_f3(f1, f2, f3, export_list, name, redo, type, dd, rr):
    # frame f3
    clear(f2)
    clear(f3)
    f3.tkraise()

    # f3 nu modifica root
    f3.pack_propagate(False)

    # widgets
    logo = ImageTk.PhotoImage(file="./pictures/logo2-01.png")
    logo_widget = tk.Label(f3, image=logo, bg="#2e525b")
    logo_widget.image = logo
    logo_widget.pack(pady=0)

    export_list = sorted(export_list, key=lambda item: (item[0], item[1], item[2]))
    if len(export_list) > 1:
        # generare date prin apelul euristicii
        if redo:
            if type:
                call_algorithm(export_list, 1)
            else:
                call_algorithm(export_list, 0)

        # preluare date generate de euristica
        f = open("output.txt", "r")
        room_list = [int(x) for x in f.readline().split()]
        room_count = max(room_list)
        if room_count == 0:
            for r in range(0, len(room_list)):
                room_list[r] = r+1
        room_count = max(room_list)

        # creare nr de camere = room_count
        rooms = []
        ROOMS = ["Toate sălile"]
        for i in range(1, room_count+1):
            room_name = "sala " + str(i)
            rooms.append(room_name)
            ROOMS.append(room_name)

        options_frame = tk.Frame(f3, bg="#2e525b")
        options_frame.pack(pady=0, fill=tk.BOTH)
        DAYS = ["Toate zilele", "Luni", "Marți", "Miercuri", "Joi", "Vineri"]
        day_variable = tk.StringVar(f3)
        room_variable = tk.StringVar(f3)
        day_variable.set(DAYS[dd])  # valori default
        room_variable.set(ROOMS[rr])
        day_filter = tk.OptionMenu(options_frame, day_variable, *DAYS)
        day_filter.pack(side=tk.LEFT, padx=40, pady=10)
        room_select = tk.OptionMenu(options_frame, room_variable, *ROOMS)
        room_select.pack(side=tk.RIGHT, padx=40, pady=10)

        busy_days = []
        if dd == 0:
            for i in range(0, len(room_list)):
                if room_list[i]:
                    if export_list[i][1] not in busy_days:
                        busy_days.append(export_list[i][1])
        else:
            busy_days.append(DAYS[dd])

        days = ["Luni", "Marți", "Miercuri", "Joi", "Vineri"]
        hours = ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]
        tree_data = []

        for d in range(0, 5):
            if days[d] in busy_days:
                # print(days[d])
                current_day = days[d]
                entry_count = 0
                for h in range(0, 6):
                    for i in range(0, len(room_list)):
                        if room_list[i] and export_list[i][1] == days[d] and export_list[i][2] == hours[h]:
                            # print(export_list[i][2] + " ... " + export_list[i][0] + " ......... " + rooms[room_list[i] - 1])
                            if entry_count == 0:
                                current_day = str(current_day)
                            else:
                                current_day = ""

                            if (rr and rooms[room_list[i] - 1] == ROOMS[rr]) or rr == 0:
                                tree_row = (current_day, export_list[i][2], export_list[i][0], rooms[room_list[i] - 1])
                                tree_data.append(tree_row)
                                entry_count += 1

        # big try of a leap - that actually worked ;)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#cce1e5", foreground="#124654", rowheight=30, fieldbackground="#cce1e5", font=("TkMenuFont", 11))
        style.configure("Treeview.Heading", foreground="#cce1e5", background="#2596be", font=("TkMenuFont", 11))
        style.map('Treeview', background=[('selected', '#124654')], foreground=[('selected', '#cce1e5')])

        time_frame = tk.Frame(f3)
        time_frame.pack(pady=10)

        time_scroll = tk.Scrollbar(time_frame)
        time_scroll.pack(side=tk.RIGHT, fill=Y)

        time_tree = ttk.Treeview(time_frame, yscrollcommand=time_scroll.set)

        time_scroll.config(command=time_tree.yview)

        # definire coloane
        time_tree['columns'] = ("Ziua", "Ora", "Materia", "Sala")
        # formatare coloane
        time_tree.column("#0", width=0, stretch=NO)
        time_tree.column("Ziua", anchor=CENTER, width=62)
        time_tree.column("Ora", anchor=CENTER, width=93)
        time_tree.column("Materia", anchor=CENTER, width=280)
        time_tree.column("Sala", anchor=CENTER, width=70)
        # creare heading
        time_tree.heading("#0", text="", anchor=W)
        time_tree.heading("Ziua", text="Ziua", anchor=CENTER)
        time_tree.heading("Ora", text="Ora", anchor=CENTER)
        time_tree.heading("Materia", text="Materia", anchor=CENTER)
        time_tree.heading("Sala", text="Sala", anchor=CENTER)
        # adaugare date
        row_count = 0
        for reg in tree_data:
            time_tree.insert(parent='', index='end', iid=str(row_count), text="", values=(reg[0], reg[1], reg[2], reg[3]))
            row_count += 1
        time_tree.pack()

        # widgets
        buttons_frame = tk.Frame(f3, bg="#2e525b")
        buttons_frame.pack(pady=0, fill=tk.BOTH)
        back_button = tk.Button(buttons_frame, text="Înapoi", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13), cursor="hand2",
                                activebackground="#badee2", activeforeground="black",
                                command=lambda: load_f2(f1, f2, f3, name))
        back_button.pack(padx=30, pady=15, side=tk.LEFT)
        again_button = tk.Button(buttons_frame, text="Filtrează orarul", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13),
                                 cursor="hand2",
                                 activebackground="#badee2", activeforeground="black",
                                 command=lambda: load_f3(f1, f2, f3, export_list, name, False, type, DAYS.index(day_variable.get()), ROOMS.index(room_variable.get())))
        again_button.pack(padx=30, pady=15, side=tk.RIGHT)
        save_button = tk.Button(buttons_frame, text="Salvează", bg="#2596be", fg="#cce1e5", font=("TkMenuFont", 13), cursor="hand2",
                                activebackground="#badee2", activeforeground="white",
                                command=lambda: save_file(export_list))
        save_button.pack(padx=20, pady=15, side=tk.RIGHT)
    else:
        instr_label = tk.Label(f3,
                               text="Nu poți genera un orar cu mai puțin de două evenimente. Reîncearcă!",
                               bg="#2e525b", fg="#cce1e5", font=("TkMenuFont", 13))
        instr_label.pack(padx=30, pady=15)

        buttons_frame = tk.Frame(f3, bg="#2e525b")
        buttons_frame.pack(pady=0, fill=tk.BOTH)
        back_button = tk.Button(buttons_frame, text="Înapoi", bg="#cce1e5", fg="#124654", font=("TkMenuFont", 13),
                                cursor="hand2",
                                activebackground="#badee2", activeforeground="black",
                                command=lambda: load_f2(f1, f2, f3, name))
        back_button.pack(padx=30, pady=15, side=tk.BOTTOM)

