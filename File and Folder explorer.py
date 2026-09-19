import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os


# =========================================================
# LOGIN DETAILS
# =========================================================

USERNAME = "admin"
PASSWORD = "1234"

current_path = None
selected_path = None


# =========================================================
# LOGIN WINDOW
# =========================================================

def login():

    username = username_entry.get()
    password = password_entry.get()

    if username == USERNAME and password == PASSWORD:

        login_window.destroy()
        open_dashboard()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password"
        )


# =========================================================
# LOGOUT
# =========================================================

def logout():

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if answer:

        dashboard.destroy()
        create_login()


# =========================================================
# RECURSIVELY LOAD FILES AND FOLDERS
# =========================================================

def load_tree(parent, path):

    try:

        items = sorted(os.listdir(path))

        for item in items:

            full_path = os.path.join(
                path,
                item
            )

            if os.path.isdir(full_path):

                folder = tree.insert(
                    parent,
                    "end",
                    text="📁 " + item,
                    values=(full_path,)
                )

                # RECURSION
                load_tree(
                    folder,
                    full_path
                )

            else:

                tree.insert(
                    parent,
                    "end",
                    text="📄 " + item,
                    values=(full_path,)
                )

    except PermissionError:
        pass


# =========================================================
# COUNT FILES AND FOLDERS USING RECURSION
# =========================================================

def count_items(path):

    files = 0
    folders = 0

    try:

        for item in os.listdir(path):

            full_path = os.path.join(
                path,
                item
            )

            if os.path.isdir(full_path):

                folders += 1

                # RECURSION
                f, d = count_items(
                    full_path
                )

                files += f
                folders += d

            else:

                files += 1

    except PermissionError:
        pass

    return files, folders


# =========================================================
# UPDATE DASHBOARD
# =========================================================

def update_dashboard():

    if not current_path:

        file_count_label.config(
            text="0"
        )

        folder_count_label.config(
            text="0"
        )

        total_count_label.config(
            text="0"
        )

        path_label.config(
            text="No folder selected"
        )

        return

    files, folders = count_items(
        current_path
    )

    file_count_label.config(
        text=str(files)
    )

    folder_count_label.config(
        text=str(folders)
    )

    total_count_label.config(
        text=str(files + folders)
    )

    path_label.config(
        text=current_path
    )


# =========================================================
# CHOOSE FOLDER
# =========================================================

def choose_folder():

    global current_path

    path = filedialog.askdirectory()

    if path:

        current_path = path

        refresh()


# =========================================================
# REFRESH
# =========================================================

def refresh():

    if not current_path:

        messagebox.showwarning(
            "Choose Folder",
            "Please choose a folder first."
        )

        return

    tree.delete(
        *tree.get_children()
    )

    root = tree.insert(
        "",
        "end",
        text="📁 " + os.path.basename(
            current_path
        ),
        values=(current_path,)
    )

    load_tree(
        root,
        current_path
    )

    tree.item(
        root,
        open=True
    )

    update_dashboard()


# =========================================================
# SHOW ALL
# =========================================================

def show_all():

    search_entry.delete(
        0,
        tk.END
    )

    refresh()


# =========================================================
# SELECT ITEM
# =========================================================

def select_item(event):

    global selected_path

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(
        selected,
        "values"
    )

    if values:

        selected_path = values[0]

        selected_label.config(
            text="Selected: " + selected_path
        )


# =========================================================
# OPEN FILE OR FOLDER
# =========================================================

def open_item(event):

    selected = tree.focus()

    if not selected:
        return

    values = tree.item(
        selected,
        "values"
    )

    if not values:
        return

    path = values[0]

    if os.path.exists(path):

        try:

            os.startfile(path)

        except Exception:

            messagebox.showerror(
                "Error",
                "Cannot open this item."
            )


# =========================================================
# SEARCH
# =========================================================

def search_files():

    name = search_entry.get().strip().lower()

    if name == "":

        messagebox.showwarning(
            "Search",
            "Enter a file or folder name."
        )

        return

    if not current_path:

        messagebox.showwarning(
            "Search",
            "Choose a folder first."
        )

        return

    tree.delete(
        *tree.get_children()
    )

    found = False

    # -----------------------------------------------------
    # RECURSIVE SEARCH
    # -----------------------------------------------------

    def search(path, parent):

        nonlocal found

        try:

            for item in os.listdir(path):

                full_path = os.path.join(
                    path,
                    item
                )

                if name in item.lower():

                    tree.insert(
                        parent,
                        "end",
                        text=(
                            "📁 "
                            if os.path.isdir(full_path)
                            else "📄 "
                        ) + item,
                        values=(full_path,)
                    )

                    found = True

                # RECURSION
                if os.path.isdir(full_path):

                    search(
                        full_path,
                        parent
                    )

        except PermissionError:
            pass

    search(
        current_path,
        ""
    )

    if not found:

        messagebox.showinfo(
            "Search",
            "File or folder not found."
        )


# =========================================================
# CLEAR SEARCH
# =========================================================

def clear_search():

    search_entry.delete(
        0,
        tk.END
    )

    refresh()


# =========================================================
# NEW FOLDER
# =========================================================

def new_folder():

    selected = tree.focus()

    if not current_path:

        messagebox.showwarning(
            "New Folder",
            "Choose a folder first."
        )

        return

    if selected:

        parent_path = tree.item(
            selected,
            "values"
        )[0]

        if not os.path.isdir(parent_path):

            messagebox.showwarning(
                "New Folder",
                "Please select a folder."
            )

            return

    else:

        parent_path = current_path

    name = name_entry.get().strip()

    if name == "":

        messagebox.showwarning(
            "New Folder",
            "Enter folder name in the Name box."
        )

        return

    new_path = os.path.join(
        parent_path,
        name
    )

    try:

        os.mkdir(new_path)

        name_entry.delete(
            0,
            tk.END
        )

        refresh()

        messagebox.showinfo(
            "Success",
            "New folder created successfully."
        )

    except FileExistsError:

        messagebox.showerror(
            "Error",
            "Folder already exists."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# =========================================================
# NEW FILE
# =========================================================

def new_file():

    selected = tree.focus()

    if not current_path:

        messagebox.showwarning(
            "New File",
            "Choose a folder first."
        )

        return

    if selected:

        parent_path = tree.item(
            selected,
            "values"
        )[0]

        if not os.path.isdir(parent_path):

            messagebox.showwarning(
                "New File",
                "Please select a folder."
            )

            return

    else:

        parent_path = current_path

    name = name_entry.get().strip()

    if name == "":

        messagebox.showwarning(
            "New File",
            "Enter file name in the Name box."
        )

        return

    new_path = os.path.join(
        parent_path,
        name
    )

    try:

        open(
            new_path,
            "w"
        ).close()

        name_entry.delete(
            0,
            tk.END
        )

        refresh()

        messagebox.showinfo(
            "Success",
            "New file created successfully."
        )

    except FileExistsError:

        messagebox.showerror(
            "Error",
            "File already exists."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# =========================================================
# RENAME
# =========================================================

def rename_item():

    selected = tree.focus()

    if not selected:

        messagebox.showwarning(
            "Rename",
            "Select the file or folder you want to rename."
        )

        return

    old_path = tree.item(
        selected,
        "values"
    )[0]

    new_name = name_entry.get().strip()

    if new_name == "":

        messagebox.showwarning(
            "Rename",
            "Enter the new name in the Name box."
        )

        return

    parent_path = os.path.dirname(
        old_path
    )

    new_path = os.path.join(
        parent_path,
        new_name
    )

    try:

        os.rename(
            old_path,
            new_path
        )

        name_entry.delete(
            0,
            tk.END
        )

        refresh()

        messagebox.showinfo(
            "Success",
            "Renamed successfully."
        )

    except FileExistsError:

        messagebox.showerror(
            "Error",
            "A file or folder with this name already exists."
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )


# =========================================================
# DELETE
# =========================================================

def delete_item():

    selected = tree.focus()

    if not selected:

        messagebox.showwarning(
            "Delete",
            "Select a file or folder first."
        )

        return

    path = tree.item(
        selected,
        "values"
    )[0]

    if path == current_path:

        messagebox.showwarning(
            "Delete",
            "You cannot delete the main selected folder."
        )

        return

    answer = messagebox.askyesno(
        "Delete",
        "Are you sure you want to delete this?"
    )

    if not answer:
        return

    try:

        if os.path.isfile(path):

            os.remove(path)

        elif os.path.isdir(path):

            os.rmdir(path)

        refresh()

        messagebox.showinfo(
            "Success",
            "Deleted successfully."
        )

    except OSError:

        messagebox.showerror(
            "Error",
            "Cannot delete this folder because it is not empty."
        )


# =========================================================
# LOGIN SCREEN
# =========================================================

def create_login():

    global login_window
    global username_entry
    global password_entry

    login_window = tk.Tk()

    login_window.title(
        "File Explorer - Login"
    )

    login_window.geometry(
        "500x500"
    )

    login_window.configure(
        bg="#eef2f7"
    )

    login_window.resizable(
        False,
        False
    )

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    header = tk.Frame(
        login_window,
        bg="#243447",
        height=110
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="📁",
        font=("Arial", 35),
        bg="#243447",
        fg="white"
    ).pack(
        pady=(15, 0)
    )

    tk.Label(
        header,
        text="FILE AND FOLDER EXPLORER",
        font=("Arial", 16, "bold"),
        bg="#243447",
        fg="white"
    ).pack()

    # -----------------------------------------------------
    # LOGIN CARD
    # -----------------------------------------------------

    card = tk.Frame(
        login_window,
        bg="white",
        bd=1,
        relief="solid"
    )

    card.pack(
        padx=55,
        pady=35,
        fill="both",
        expand=True
    )

    tk.Label(
        card,
        text="Welcome Back!",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#243447"
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        card,
        text="Login to access your files and folders",
        font=("Arial", 10),
        bg="white",
        fg="#6b7280"
    ).pack(
        pady=(0, 20)
    )

    # Username

    tk.Label(
        card,
        text="Username",
        font=("Arial", 10, "bold"),
        bg="white",
        anchor="w"
    ).pack(
        fill="x",
        padx=45
    )

    username_entry = tk.Entry(
        card,
        font=("Arial", 11),
        bd=1,
        relief="solid"
    )

    username_entry.pack(
        padx=45,
        pady=(5, 15),
        ipady=6,
        fill="x"
    )

    # Password

    tk.Label(
        card,
        text="Password",
        font=("Arial", 10, "bold"),
        bg="white",
        anchor="w"
    ).pack(
        fill="x",
        padx=45
    )

    password_entry = tk.Entry(
        card,
        font=("Arial", 11),
        show="*",
        bd=1,
        relief="solid"
    )

    password_entry.pack(
        padx=45,
        pady=(5, 20),
        ipady=6,
        fill="x"
    )

    # Login button

    tk.Button(
        card,
        text="LOGIN",
        font=("Arial", 11, "bold"),
        bg="#2e86de",
        fg="white",
        activebackground="#1b4f72",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=login
    ).pack(
        padx=45,
        fill="x",
        ipady=8
    )

    tk.Label(
        card,
        text="Demo Login: admin / 1234",
        font=("Arial", 9),
        bg="white",
        fg="#7f8c8d"
    ).pack(
        pady=15
    )

    login_window.bind(
        "<Return>",
        lambda event: login()
    )

    login_window.mainloop()


# =========================================================
# MAIN DASHBOARD
# =========================================================

def open_dashboard():

    global dashboard
    global tree
    global file_count_label
    global folder_count_label
    global total_count_label
    global path_label
    global selected_label
    global search_entry
    global name_entry

    dashboard = tk.Tk()

    dashboard.title(
        "File and Folder Explorer Dashboard"
    )

    dashboard.geometry(
        "1150x780"
    )

    dashboard.configure(
        bg="#eef2f7"
    )

    # =====================================================
    # HEADER
    # =====================================================

    header = tk.Frame(
        dashboard,
        bg="#243447",
        height=70
    )

    header.pack(
        fill="x"
    )

    tk.Label(
        header,
        text="📁 FILE AND FOLDER EXPLORER",
        font=("Arial", 19, "bold"),
        bg="#243447",
        fg="white"
    ).pack(
        side="left",
        padx=25,
        pady=18
    )

    tk.Button(
        header,
        text="Logout",
        font=("Arial", 10, "bold"),
        bg="#e74c3c",
        fg="white",
        activebackground="#c0392b",
        activeforeground="white",
        bd=0,
        cursor="hand2",
        command=logout
    ).pack(
        side="right",
        padx=25
    )

    # =====================================================
    # WELCOME
    # =====================================================

    welcome = tk.Frame(
        dashboard,
        bg="#eef2f7"
    )

    welcome.pack(
        fill="x",
        padx=30,
        pady=(15, 5)
    )

    tk.Label(
        welcome,
        text="Welcome, Admin 👋",
        font=("Arial", 18, "bold"),
        bg="#eef2f7",
        fg="#243447"
    ).pack(
        side="left"
    )

    # =====================================================
    # DASHBOARD CARDS
    # =====================================================

    cards = tk.Frame(
        dashboard,
        bg="#eef2f7"
    )

    cards.pack(
        fill="x",
        padx=25,
        pady=10
    )

    # Files

    file_card = tk.Frame(
        cards,
        bg="#3498db",
        height=105
    )

    file_card.grid(
        row=0,
        column=0,
        padx=8,
        sticky="nsew"
    )

    tk.Label(
        file_card,
        text="📄  FILES",
        font=("Arial", 11, "bold"),
        bg="#3498db",
        fg="white"
    ).pack(
        pady=(12, 0)
    )

    file_count_label = tk.Label(
        file_card,
        text="0",
        font=("Arial", 26, "bold"),
        bg="#3498db",
        fg="white"
    )

    file_count_label.pack()

    # Folders

    folder_card = tk.Frame(
        cards,
        bg="#27ae60",
        height=105
    )

    folder_card.grid(
        row=0,
        column=1,
        padx=8,
        sticky="nsew"
    )

    tk.Label(
        folder_card,
        text="📁  FOLDERS",
        font=("Arial", 11, "bold"),
        bg="#27ae60",
        fg="white"
    ).pack(
        pady=(12, 0)
    )

    folder_count_label = tk.Label(
        folder_card,
        text="0",
        font=("Arial", 26, "bold"),
        bg="#27ae60",
        fg="white"
    )

    folder_count_label.pack()

    # Total

    total_card = tk.Frame(
        cards,
        bg="#8e44ad",
        height=105
    )

    total_card.grid(
        row=0,
        column=2,
        padx=8,
        sticky="nsew"
    )

    tk.Label(
        total_card,
        text="📊  TOTAL ITEMS",
        font=("Arial", 11, "bold"),
        bg="#8e44ad",
        fg="white"
    ).pack(
        pady=(12, 0)
    )

    total_count_label = tk.Label(
        total_card,
        text="0",
        font=("Arial", 26, "bold"),
        bg="#8e44ad",
        fg="white"
    )

    total_count_label.pack()

    cards.columnconfigure(
        0,
        weight=1
    )

    cards.columnconfigure(
        1,
        weight=1
    )

    cards.columnconfigure(
        2,
        weight=1
    )

    # =====================================================
    # CURRENT PATH
    # =====================================================

    path_frame = tk.Frame(
        dashboard,
        bg="white",
        bd=1,
        relief="solid"
    )

    path_frame.pack(
        fill="x",
        padx=30,
        pady=5
    )

    tk.Label(
        path_frame,
        text="📍 Current Folder:",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#243447"
    ).pack(
        side="left",
        padx=12,
        pady=10
    )

    path_label = tk.Label(
        path_frame,
        text="No folder selected",
        font=("Arial", 10),
        bg="white",
        fg="#555555"
    )

    path_label.pack(
        side="left"
    )

    # =====================================================
    # TOP BUTTONS
    # =====================================================

    top_buttons = tk.Frame(
        dashboard,
        bg="#eef2f7"
    )

    top_buttons.pack(
        pady=8
    )

    tk.Button(
        top_buttons,
        text="📂 Choose Folder",
        width=16,
        bg="#2e86de",
        fg="white",
        bd=0,
        command=choose_folder
    ).grid(
        row=0,
        column=0,
        padx=4
    )

    tk.Button(
        top_buttons,
        text="🔄 Refresh",
        width=13,
        bg="#f39c12",
        fg="white",
        bd=0,
        command=refresh
    ).grid(
        row=0,
        column=1,
        padx=4
    )

    tk.Button(
        top_buttons,
        text="📋 Show All",
        width=13,
        bg="#16a085",
        fg="white",
        bd=0,
        command=show_all
    ).grid(
        row=0,
        column=2,
        padx=4
    )

    # =====================================================
    # SEARCH
    # =====================================================

    search_frame = tk.Frame(
        dashboard,
        bg="#eef2f7"
    )

    search_frame.pack(
        pady=5
    )

    tk.Label(
        search_frame,
        text="🔍 Search:",
        font=("Arial", 10, "bold"),
        bg="#eef2f7"
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 10)
    )

    search_entry.grid(
        row=0,
        column=1,
        padx=5,
        ipady=4
    )

    tk.Button(
        search_frame,
        text="Search",
        width=10,
        bg="#3498db",
        fg="white",
        bd=0,
        command=search_files
    ).grid(
        row=0,
        column=2,
        padx=3
    )

    tk.Button(
        search_frame,
        text="Clear",
        width=10,
        bg="#95a5a6",
        fg="white",
        bd=0,
        command=clear_search
    ).grid(
        row=0,
        column=3,
        padx=3
    )

    # =====================================================
    # NAME BOX
    # =====================================================

    name_frame = tk.Frame(
        dashboard,
        bg="#eef2f7"
    )

    name_frame.pack(
        pady=4
    )

    tk.Label(
        name_frame,
        text="Name:",
        font=("Arial", 10, "bold"),
        bg="#eef2f7"
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    name_entry = tk.Entry(
        name_frame,
        width=35,
        font=("Arial", 10)
    )

    name_entry.grid(
        row=0,
        column=1,
        padx=5,
        ipady=4
    )

    # =====================================================
    # OPERATION BUTTONS
    # =====================================================

    operation_frame = tk.Frame(
        dashboard,
        bg="#eef2f7"
    )

    operation_frame.pack(
        pady=6
    )

    tk.Button(
        operation_frame,
        text="➕ New Folder",
        width=15,
        bg="#27ae60",
        fg="white",
        bd=0,
        command=new_folder
    ).grid(
        row=0,
        column=0,
        padx=4
    )

    tk.Button(
        operation_frame,
        text="📄 New File",
        width=15,
        bg="#2980b9",
        fg="white",
        bd=0,
        command=new_file
    ).grid(
        row=0,
        column=1,
        padx=4
    )

    tk.Button(
        operation_frame,
        text="✏ Rename",
        width=15,
        bg="#f39c12",
        fg="white",
        bd=0,
        command=rename_item
    ).grid(
        row=0,
        column=2,
        padx=4
    )

    tk.Button(
        operation_frame,
        text="🗑 Delete",
        width=15,
        bg="#e74c3c",
        fg="white",
        bd=0,
        command=delete_item
    ).grid(
        row=0,
        column=3,
        padx=4
    )

    # =====================================================
    # TREE AREA
    # =====================================================

    tree_frame = tk.Frame(
        dashboard,
        bg="white",
        bd=1,
        relief="solid"
    )

    tree_frame.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=8
    )

    tk.Label(
        tree_frame,
        text="  🌳 Folder Structure",
        font=("Arial", 12, "bold"),
        bg="#dfe6e9",
        fg="#243447",
        anchor="w"
    ).pack(
        fill="x"
    )

    tree_area = tk.Frame(
        tree_frame,
        bg="white"
    )

    tree_area.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    tree = ttk.Treeview(
        tree_area
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = ttk.Scrollbar(
        tree_area,
        orient="vertical",
        command=tree.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    # =====================================================
    # SELECTED ITEM
    # =====================================================

    selected_label = tk.Label(
        dashboard,
        text="Selected: None",
        font=("Arial", 9),
        bg="#eef2f7",
        fg="#555555",
        anchor="w"
    )

    selected_label.pack(
        fill="x",
        padx=30,
        pady=(0, 8)
    )

    # =====================================================
    # TREE EVENTS
    # =====================================================

    tree.bind(
        "<<TreeviewSelect>>",
        select_item
    )

    tree.bind(
        "<Double-1>",
        open_item
    )

    dashboard.mainloop()


# =========================================================
# START PROGRAM
# =========================================================

create_login()