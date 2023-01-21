import pickle
import random
import tkinter as tk
from datetime import date
from tkinter import ttk


def cypher_machine_storage(username):
    # File Integrity 'Check'
    with open(username, "rb") as handle:
        try:
            enigma_dict = pickle.load(handle)
        except EOFError:
            enigma_dict = {"Empty": " "}

    if len(enigma_dict.keys()) == 0:
        enigma_dict = {"Empty": ""}

    def del_service_name_input(arg):
        """
        Del input with 'Service Name' after click
        :param arg:
        :return:
        """
        input_service.delete(0, "end")

    def del_empty():
        """
        Removes an extra value after checking the integrity of the file
        :return:
        """
        if "Empty" in enigma_dict:
            del enigma_dict["Empty"]

    def del_service():
        """
        1. Dell element from File
        2. Check dict for empty items
        3. Update data in 'OptionMenu'
        :return:
        """
        del enigma_dict[clicked.get()]
        pickle.dump(enigma_dict, open(username, "wb"), protocol=pickle.HIGHEST_PROTOCOL)
        btn_view["state"] = tk.DISABLED
        btn_del["state"] = tk.DISABLED
        # If data empty - append item for option menu
        dict_check = list(enigma_dict.keys())
        if len(dict_check) == 0:
            enigma_dict[""] = ""
        # Update Option Menu
        clicked.set("Choose:")
        option_menu_post_del = tk.OptionMenu(tab2, clicked, *enigma_dict, command=switch_btn_view)
        option_menu_post_del.grid(row=1, column=1, sticky="w")
        option_menu_post_del.config(font=font_text)
        menu_widget_del = tab2.nametowidget(option_menu_post_del.menuname)
        menu_widget_del.config(font=font_text)
        # If data empty
        if len(dict_check) == 0:
            del enigma_dict[""]
            option_menu_post_del["state"] = tk.DISABLED
        # Generate empty input:
        place4pass_post_del = tk.Text(tab2, height=1, width=30)
        place4pass_post_del.grid(row=3, column=1, sticky="w")
        place4pass_post_del.config(font=font_text, state=tk.DISABLED)

    def last_pass(service_name):
        """
        Use custom formula and generate pass.
        :param service_name: from input
        :return:pass
        """
        d = date.today()
        combine_string = service_name.get() + str(d) + "Bil|"
        row_pass = random.sample(list(combine_string), len(combine_string))
        new_pass = ""
        for item in list(row_pass):
            new_pass += item
        return new_pass

    def save_pass():
        """
        1. Add element to File
        2. Run fn del_empty
        3. Update data in 'OptionMenu'
        :return:
        """
        # Add item {'Name_Service': 'Pass_Service'} to Dict
        enigma_dict[input_var.get()] = place4pass_generate.get("1.0", "end")
        # Delete Empty key:
        del_empty()
        # Load and write data.txt to dict
        pickle.dump(enigma_dict, open(username, "wb"), protocol=pickle.HIGHEST_PROTOCOL)
        # Create new option menu with update data
        clicked.set("Choose:")
        option_menu_post_save = tk.OptionMenu(tab2, clicked, *enigma_dict, command=switch_btn_view)
        option_menu_post_save.config(font=font_text)
        option_menu_post_save.grid(row=1, column=1, sticky="w")
        menu_widget_save = tab2.nametowidget(option_menu_post_save.menuname)
        menu_widget_save.config(font=font_text)

    def view_pass():
        """
        Generate input with saved 'pass'
        :return:
        """
        place4pass_data = tk.Text(tab2, height=1, width=30)
        place4pass_data.grid(row=3, column=1, sticky="w")
        place4pass_data.insert(tk.END, enigma_dict[clicked.get()])
        place4pass_data.config(font=font_text, state=tk.DISABLED)

    def place4pass():
        """
        Generate input with 'new pass'
        :return:
        """
        place4pass_generate.config(state=tk.NORMAL)
        place4pass_generate.delete("1.0", "end")
        place4pass_generate.insert(tk.END, last_pass(input_var))
        place4pass_generate.config(state=tk.DISABLED)

    def switch_btn_view(arg):
        """
        Monitoring the state of interface elements after a change 'File'
        :param arg:
        :return:
        """
        if "Choose" in enigma_dict:
            btn_view["state"] = tk.DISABLED
            btn_del["state"] = tk.DISABLED
        elif "Empty" in enigma_dict:
            option_menu_base["state"] = tk.DISABLED
            btn_view["state"] = tk.DISABLED
            btn_del["state"] = tk.DISABLED
        elif len(enigma_dict.keys()) == 0:
            btn_view["state"] = tk.DISABLED
            btn_del["state"] = tk.DISABLED
        else:
            btn_view["state"] = tk.NORMAL
            btn_del["state"] = tk.NORMAL
            place4pass_data = tk.Text(tab2, height=1, width=30)
            place4pass_data.grid(row=3, column=1, sticky="w")
            place4pass_data.config(font=font_text, state=tk.DISABLED)

    # Main: Create Main window and setting up.
    cypher_machine = tk.Tk()
    cypher_machine.geometry("600x250")
    cypher_machine.title("Cypher Machine")
    cypher_machine.resizable(width=False, height=False)

    font_text = ("Roboto", 9)
    font_title = ("Roboto", 11, "bold")

    # Add dynamic 'Attrs'
    input_var = tk.StringVar()
    clicked = tk.StringVar()

    #  Create Tabs (Frame)
    tab_control = ttk.Notebook(cypher_machine)
    cypher_machine.tk.call('wm', 'iconphoto', cypher_machine, tk.PhotoImage(file='favicon.png'))

    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)

    tab_control.add(tab1, text="Generate Pass")
    tab_control.add(tab2, text="View My Pass")
    tab_control.pack(expand=1, fill="both")

    # Tab1: Create place and add elements
    tab1.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
    tab1.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)

    label4service = tk.Label(tab1, text="Service Name: ", font=font_title)
    label4service.grid(row=0, column=1, sticky="ws")

    # Generate input with 'Name services'
    input_service = tk.Entry(tab1, textvariable=input_var, font=font_text, width=30)
    input_service.config(font=font_text)
    input_service.grid(row=1, column=1, sticky="w")
    input_service.insert(0, "Enter service")
    input_service.bind('<FocusIn>', del_service_name_input)

    # Generate button 'Generate'
    btn_generate = tk.Button(tab1, text="Generate", command=place4pass)
    btn_generate.config(width=8, font=font_text, cursor="exchange")
    btn_generate.grid(row=1, column=3, sticky="e")

    label4pass = tk.Label(tab1, text="Your Pass: ", font=font_title)
    label4pass.grid(row=2, column=1, sticky="ws")

    # Generate input with 'pass'
    place4pass_generate = tk.Text(tab1, font=font_text, height=1, width=30)
    place4pass_generate.grid(row=3, column=1, sticky="w")
    place4pass_generate.config(state=tk.DISABLED)

    # Generate button 'Save'
    btn_save = tk.Button(master=tab1, text='Save', command=save_pass)
    btn_save.config(width=8, font=font_text, cursor="hand2")
    btn_save.grid(row=3, column=3, sticky="e")

    # Tab2: Create place and add elements
    tab2.rowconfigure([0, 1, 2, 3, 4], minsize=50, weight=1)
    tab2.columnconfigure([0, 1, 2, 3, 4, 5, 6], minsize=50, weight=1)

    label4service = tk.Label(tab2, text="Service Name: ", font=font_title)
    label4service.grid(row=0, column=1, sticky="ws")

    # Generate option menu with 'Services'
    clicked.set("Choose:")
    option_menu_base = tk.OptionMenu(tab2, clicked, *enigma_dict, command=switch_btn_view)
    option_menu_base.config(font=font_text)
    option_menu_base.grid(row=1, column=1, sticky="w")
    menu_widget_base = tab2.nametowidget(option_menu_base.menuname)
    menu_widget_base.config(font=font_text)

    # Generate button "View'
    btn_view = tk.Button(tab2, text="View", state=tk.DISABLED, command=view_pass)
    btn_view.config(width=8, font=font_text, cursor="hand2")
    btn_view.grid(row=1, column=3, sticky="w")

    label4service = tk.Label(tab2, text="Your Pass: ", font=font_title)
    label4service.grid(row=2, column=1, sticky="ws")

    # Generate input with 'pass'
    place4pass_data = tk.Text(tab2, height=1, width=30)
    place4pass_data.grid(row=3, column=1, sticky="w")
    place4pass_data.config(font=font_text, state=tk.DISABLED)

    # Generate button "Delete'
    btn_del = tk.Button(tab2, text="Delete", width=8, command=del_service)
    btn_del.config(width=8, font=font_text, cursor="pirate", state=tk.DISABLED)
    btn_del.grid(row=3, column=3, sticky="w")

    cypher_machine.mainloop()


