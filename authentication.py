import tkinter as tk
import pickle
from tkinter import ttk
from cipher_machine import cypher_machine_storage


# File Integrity 'Check'
try:
    start_dict_user = pickle.load(open("enigma_log_user.txt", "rb"))
except (OSError, IOError):
    start_dict_user = {}
    pickle.dump(start_dict_user, open("enigma_log_user.txt", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
    del start_dict_user[""]


def control_login_input(arg):
    """
    Delete input 'login'
    :param arg: None
    :return:
    """
    username_input.delete(0, "end")


def control_pass_input(arg):
    """
    1. Delete input 'pass'
    2. Hide password
    3. Active button 'Sign In'
    :param arg: None
    :return:
    """
    password_input.delete(0, "end")
    password_input.config(show='*')
    btn_sign_in['state'] = tk.NORMAL


def control_new_login_input(arg):
    """
    1. Active input 'pass 1'
    2. Hide password
    :param arg: None
    :return:
    """
    # new_username_input.delete(0, "end")
    new_password_1_input["state"] = tk.NORMAL
    new_password_1_input.config(show='*')


def control_new_pass1_input(arg):
    """
    1. Active input 'pass 2'
    2. Hide password
    :param arg: None
    :return:
    """
    new_password_2_input["state"] = tk.NORMAL
    new_password_2_input.config(show='*')


def control_new_pass2_input(arg):
    """
    Active button 'Sign Up'
    :param arg:
    :return:
    """
    btn_sign_up["state"] = tk.NORMAL


def check_new_pass():
    """
    Checking for password matching
    :return: equal password
    """
    entered_pass_1 = new_password_1.get()
    entered_pass_2 = new_password_2.get()
    if entered_pass_1 == entered_pass_2:
        new_password = entered_pass_1
        create_user(new_password)
    else:
        print("Password_1 isn't equal to Password_2")


def create_user(confirmed_pass):
    """
    1. Check for the presence of such a login
    2. Add username's storage
    3. Clear inputs
    :param confirmed_pass:
    :return:
    """
    create_dict_users = pickle.load(open("enigma_log_user.txt", "rb"))
    entered_login = new_username.get()
    entered_pass = confirmed_pass
    if entered_login in list(create_dict_users.keys()):
        print("This user is already in the data. Please enter a different username.")
    else:
        # Create file 'username_log.txt'
        create_dict_users[entered_login] = entered_pass
        pickle.dump(create_dict_users, open("enigma_log_user.txt", "wb"), protocol=pickle.HIGHEST_PROTOCOL)
        active_user = entered_login + "_log.txt"
        open(active_user, "wb")
        # Clear inputs in 'Sign Ip'
        new_username_input.delete(0, "end")
        new_password_1_input.delete(0, "end")
        new_password_2_input.delete(0, "end")


def check_login():
    """
    1. Authentication
    2. Open username's storage
    :return:
    """
    sign_in_dict_users = pickle.load(open("enigma_log_user.txt", "rb"))
    entered_login = username.get()
    entered_pass = password.get()
    if entered_login in list(sign_in_dict_users.keys()) and sign_in_dict_users[entered_login] == entered_pass:
        active_user = entered_login + "_log.txt"
        authentication.destroy()
        cypher_machine_storage(active_user)


# Authentication - Sign In / Sign Up
authentication = tk.Tk()
authentication.geometry("600x250")
authentication.title("Login")
authentication.tk.call('wm', 'iconphoto', authentication, tk.PhotoImage(file='favicon.png'))

font_text = ("Roboto", 9)
font_title = ("Roboto", 11, "bold")

# Add dynamic 'Attrs'
username = tk.StringVar()
password = tk.StringVar()
new_username = tk.StringVar()
new_password_1 = tk.StringVar()
new_password_2 = tk.StringVar()

#  Create Tabs (Frame)
tab_control = ttk.Notebook(authentication)
tab3 = ttk.Frame(tab_control)
tab4 = ttk.Frame(tab_control)

tab_control.add(tab3, text="Sign In")
tab_control.add(tab4, text="Sign Up")
tab_control.pack(expand=1, fill="both")


# Tab3: Create place and add elements
tab3.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
tab3.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)

login_label = tk.Label(tab3, text="Your username: ", font=font_title)
login_label.grid(row=0, column=1, sticky="ws")

# Generate input with 'Enter Username'
username_input = tk.Entry(tab3, textvariable=username, width=30, font=font_text)
username_input.grid(row=1, column=1, sticky="w")
username_input.insert(0, "Enter username")
username_input.bind('<FocusIn>', control_login_input)

password_label = tk.Label(tab3, text="Your Pass: ", font=font_title)
password_label.grid(row=2, column=1, sticky="ws")

# Generate input with 'Enter Pass'
password_input = tk.Entry(tab3, textvariable=password, font=font_text, width=30)
password_input.grid(row=3, column=1, sticky="w")
password_input.insert(0, "Enter pass")
password_input.bind('<FocusIn>', control_pass_input)

# Generate button 'Sign In'
btn_sign_in = tk.Button(tab3, text="Sign In", state=tk.NORMAL, command=check_login)
btn_sign_in.config(width=8, font=font_text, cursor='hand2', state=tk.DISABLED)
btn_sign_in.grid(row=1, column=3, sticky="w")


# Tab4: Create place and add elements
tab4.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
tab4.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)

login_label = tk.Label(tab4, text="New username: ", font=font_title)
login_label.grid(row=0, column=1, sticky="ws")

# Generate input with 'Enter Username'
new_username_input = tk.Entry(tab4, textvariable=new_username, width=30, font=font_text)
new_username_input.grid(row=1, column=1, sticky="w")
new_username_input.bind('<FocusIn>', control_new_login_input)

password_label = tk.Label(tab4, text="New Pass twice: ", font=font_title)
password_label.grid(row=0, column=3, sticky="ws")

# Generate input with 'Enter New Pass #1'
new_password_1_input = tk.Entry(tab4, textvariable=new_password_1, font=font_text, width=30)
new_password_1_input.grid(row=1, column=3, sticky="w")
new_password_1_input.config(state=tk.DISABLED)
new_password_1_input.bind('<FocusIn>', control_new_pass1_input)

# Generate input with 'Enter New Pass #2'
new_password_2_input = tk.Entry(tab4, textvariable=new_password_2, font=font_text, width=30)
new_password_2_input.grid(row=2, column=3, sticky="w")
new_password_2_input.config(state=tk.DISABLED)
new_password_2_input.bind('<FocusIn>', control_new_pass2_input)

# Generate button 'Sign Up'
btn_sign_up = tk.Button(tab4, text="Sign Up", state=tk.NORMAL, command=check_new_pass)
btn_sign_up.config(width=8, font=font_text, cursor='hand2')
btn_sign_up.config(state=tk.DISABLED)
btn_sign_up.grid(row=2, column=1, sticky="w")

authentication.mainloop()


