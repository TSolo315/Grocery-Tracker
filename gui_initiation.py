from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sortable_table
import autocomplete_entry_widget
from datetime import datetime


class MainGUI:
    def __init__(self, master, settings_manager, database_manager):
        self.master = master
        self.DBM = database_manager
        self.SM = settings_manager

        self.name_list = self.DBM.get_product_name_list()
        self.store_list = self.DBM.get_store_list()
        self.username_list = self.DBM.get_user_list()
        self.transaction_dict = {}
        self.today_date = datetime.today().strftime("%Y-%m-%d")

        self.active_user = self.SM.active_user

        master.title("Grocery Tracker: " + self.active_user)
        master.geometry("1200x800")
        main_background_color = '#4b130c'
        main_foreground_color = '#FFFAFA'

        self.mainframe = Frame(self.master, height=1200, width=800, bg=main_background_color)
        self.mainframe.grid(row=0, column=0, rowspan=10, columnspan=20, sticky=W + E + N + S, padx=0, pady=0)
        self.settings_button = Button(self.mainframe, text="Settings", font="helvetica", command=self.open_settings_menu)
        self.settings_button.grid(row=0, column=0, columnspan=2, sticky=W, padx=(10, 0), pady=(10, 0))
        self.item_label = Label(self.mainframe, text='Item:', bg=main_background_color, fg=main_foreground_color)
        self.item_label.grid(row=1, column=0, sticky=W, padx=(10, 0), pady=(5, 5))
        self.item_entry = autocomplete_entry_widget.AutocompleteEntry(self.name_list, self.mainframe)
        self.item_entry.grid(row=1, column=1, sticky=W, padx=(0, 0), pady=(5, 5))
        self.price_label = Label(self.mainframe, text='Price:', bg=main_background_color, fg=main_foreground_color)
        self.price_label.grid(row=1, column=2, sticky=W, padx=(0, 0), pady=(5, 5))
        self.price_entry = Entry(self.mainframe)
        self.price_entry.grid(row=1, column=3, sticky=W, padx=(0, 0), pady=(5, 5))
        self.quantity_label = Label(self.mainframe, text='Quantity:', bg=main_background_color, fg=main_foreground_color)
        self.quantity_label.grid(row=1, column=4, sticky=W, padx=(0, 0), pady=(5, 5))
        self.quantity_entry = Entry(self.mainframe)
        self.quantity_entry.grid(row=1, column=5, sticky=W, padx=(0, 0), pady=(5, 5))
        self.quantity_entry.insert(0, '1')
        self.weight_label = Label(self.mainframe, text='Weight (lb):', bg=main_background_color, fg=main_foreground_color)
        self.weight_label.grid(row=1, column=6, sticky=W, padx=(0, 0), pady=(5, 5))
        self.weight_entry = Entry(self.mainframe)
        self.weight_entry.grid(row=1, column=7, sticky=W, padx=(0, 0), pady=(5, 5))
        self.category_label = Label(self.mainframe, text='Category:', bg=main_background_color, fg=main_foreground_color)
        self.category_label.grid(row=1, column=8, sticky=W, padx=(0, 0), pady=(5, 5))
        self.category_box = Combobox(self.mainframe, textvariable='item_category', state="readonly")
        self.category_box['values'] = ('0.5 seconds', '1 seconds', '2 seconds', '3 seconds', '4 seconds', '5 seconds', '10 seconds', '20 seconds', '30 seconds', '60 seconds')
        self.category_box.current(0)
        self.category_box.grid(row=1, column=9, columnspan=1, sticky=W, padx=0, pady=(10, 5))
        self.item_submit_button = Button(self.mainframe, text="Submit", command=self.submit_item_entry)
        self.item_submit_button.grid(row=1, column=10, sticky=W, padx=0, pady=(10, 5))

        self.transaction_box = sortable_table.Multicolumn_Listbox(self.mainframe, ["Item", "Price", "Quantity", "Category"], stripped_rows=("white", "#f2f2f2"), height=16, cell_anchor="center")
        self.transaction_box.interior.column(0, width=250)
        self.transaction_box.interior.column(1, width=100)
        self.transaction_box.interior.column(2, width=50)
        self.transaction_box.interior.column(3, width=150)
        self.transaction_box.interior.grid(row=2, rowspan=8, column=0, columnspan=10, sticky=W + N + S + E, padx=(10,5), pady=5)

        self.store_label = Label(self.mainframe, text='Store:', bg=main_background_color, fg=main_foreground_color)
        self.store_label.grid(row=10, column=0, sticky=W, padx=(10, 0), pady=(10, 10))
        self.store_box = Combobox(self.mainframe, textvariable='transaction_store', state="readonly")
        self.store_box['values'] = self.store_list
        self.store_box.current(0)
        self.store_box.grid(row=10, column=1, sticky=W, padx=0, pady=(10, 10))
        self.date_label = Label(self.mainframe, text='Date:', bg=main_background_color, fg=main_foreground_color)
        self.date_label.grid(row=10, column=2, sticky=W, padx=(10, 0), pady=(10, 10))
        self.date_entry = Entry(self.mainframe)
        self.date_entry.grid(row=10, column=3, sticky=W, padx=(0, 0), pady=(10, 10))
        self.date_entry.insert(0, self.today_date)
        self.transaction_submit_button = Button(self.mainframe, text="Submit Transaction", command=self.submit_transaction)
        self.transaction_submit_button.grid(row=10, column=9, sticky=E, padx=(0,5), pady=(10, 10))

        for i in range(0, 20):
            master.grid_columnconfigure(i, weight=1)
            self.mainframe.grid_columnconfigure(i, weight=1)
        for i in range(0, 10):
            master.grid_rowconfigure(i, weight=1)
            self.mainframe.grid_rowconfigure(i, weight=1)

        master.update()

    def open_settings_menu(self):

        def add_user_menu():

            def add_new_user():
                new_username = username_entry.get()
                if not new_username:
                    return  # Error Message?
                self.DBM.push_new_user(new_username)
                self.DBM.save()
                self.username_list.append(new_username)
                if username_box:
                    username_box['values'] = self.username_list
                    username_box.current(len(self.username_list) - 1)
                au_menu.destroy()

            def close_new_user_menu():
                au_menu.destroy()

            xx = self.master.winfo_x()
            yy = self.master.winfo_y()
            dxx = 30
            dyy = 30
            au_menu = Toplevel(height=400, width=400)
            au_menu.transient(settings_menu)
            au_menu.title("Add User")
            au_menu.update()
            au_menu.geometry("+%d+%d" % (xx + dxx, yy + dyy))

            username_label = Label(au_menu, text='Username:')
            username_label.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
            username_entry = Entry(au_menu)
            username_entry.grid(row=0, column=1, sticky=W, padx=(5, 5), pady=(10, 0))
            username_buttons_frame = Frame(au_menu)
            username_buttons_frame.grid(row=1, column=0, columnspan=2, sticky=W + E + N + S, padx=0, pady=0)
            add_new_user_button = Button(username_buttons_frame, text="Add User", command=add_new_user)
            add_new_user_button.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=10)
            close_new_user_button = Button(username_buttons_frame, text="Close", command=close_new_user_menu)
            close_new_user_button.grid(row=0, column=1, sticky=W, padx=(5, 5), pady=10)

        def add_store_menu():
            pass

        def save_settings():
            pass

        def close_settings_menu():
            settings_menu.destroy()

        color_list = ['Red', 'Blue', 'Black', 'Grey', 'Orange', 'Pink', 'Green', 'Purple']
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        dx = 30
        dy = 30
        settings_menu = Toplevel(height=400, width=400)
        settings_menu.transient(self.master)
        settings_menu.title("Settings")
        settings_menu.update()
        settings_menu.geometry("+%d+%d" % (x + dx, y + dy))

        userbox_label = Label(settings_menu, text='User:')
        userbox_label.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
        username_box = Combobox(settings_menu, textvariable='username', state="readonly")
        username_box['values'] = self.username_list
        username_box.current(0)
        username_box.grid(row=0, column=1, sticky=W, padx=(0, 10), pady=(10, 10))
        background_color_label = Label(settings_menu, text='Background Color:')
        background_color_label.grid(row=1, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
        background_color_box = Combobox(settings_menu, textvariable='bgcolor', state="readonly")
        background_color_box['values'] = color_list
        background_color_box.current(0)
        background_color_box.grid(row=1, column=1, sticky=W, padx=(0, 10), pady=(10, 10))
        settings_button_frame = Frame(settings_menu)
        settings_button_frame.grid(row=2, column=0, columnspan=2, sticky=W + E + N + S, padx=0, pady=0)
        save_settings_button = Button(settings_button_frame, text="Save", command=save_settings)
        save_settings_button.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=(5, 10))
        add_user_button = Button(settings_button_frame, text="Add User", command=add_user_menu)
        add_user_button.grid(row=0, column=1, sticky=W, padx=(5, 5), pady=(5, 10))
        add_store_button = Button(settings_button_frame, text="Add Store", command=add_store_menu)
        add_store_button.grid(row=0, column=2, sticky=W, padx=(5, 5), pady=(5, 10))
        close_settings_button = Button(settings_button_frame, text="Close", command=close_settings_menu)
        close_settings_button.grid(row=0, column=3, sticky=W, padx=(5, 10), pady=(5, 10))

    def valid_number_test(self, source_input, is_float=True, entry_name='Entry'):
        if is_float:
            try:
                testvar = float(source_input)
            except ValueError:
                print(entry_name + ' does not contain a valid number!')
                return False
        else:
            try:
                testvar = int(source_input)
            except ValueError:
                print(entry_name + ' does not contain a valid number!')
                return False
        return True

    def validate_date_format(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    def fill_transaction_box(self, transaction_dict):
        transaction_list = []
        for key, value in transaction_dict.items():
            group_listing = [key]
            group_listing.extend(value)
            transaction_list.append(group_listing)
        for i in transaction_list:
            self.transaction_box.insert_row([i[0], i[1], i[2], i[3]])

    def submit_item_entry(self):
        item_name = self.item_entry.get()
        item_price = self.price_entry.get()
        if not self.valid_number_test(item_price, entry_name='Price entry'):
            return
        item_quantity = self.quantity_entry.get()
        if not self.valid_number_test(item_quantity, is_float=False, entry_name='Quantity entry'):
            return
        item_weight = self.weight_entry.get()
        if item_weight and item_weight != '0':
            if not self.valid_number_test(item_weight, entry_name='Weight entry'):
                return
            item_price = '$' + str(round(float(item_price) / float(item_weight), 2)) + '/lb'
            weight_based_price = True
        else:
            item_price = "$" + item_price
            weight_based_price = False
        item_category = self.category_box.get()
        self.transaction_box.clear()
        self.transaction_dict.setdefault(item_name, [item_price, item_quantity, item_category, weight_based_price, item_weight])
        self.fill_transaction_box(self.transaction_dict)
        self.item_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.quantity_entry.insert(0, '1')
        self.weight_entry.delete(0, END)
        self.category_box.current(0)

    def submit_transaction(self):
        if len(self.transaction_dict) < 1:
            print('Empty Transaction')
            return
        store = self.store_box.get()  # Add idiot tests.
        date = self.date_entry.get()
        transaction_list = []
        transaction_total = 0
        for key, value in self.transaction_dict.items():
            group_listing = [key.lower()]
            group_listing.extend(value)
            if group_listing[4]:
                group_listing[1] = group_listing[1].replace('/lb', '')
            group_listing[1] = group_listing[1].replace('$', '')
            transaction_list.append(group_listing)
        for i in transaction_list:
            self.DBM.update_product(i) if i[0] in self.name_list else self.DBM.push_product(i)
            self.DBM.push_transaction(i, self.active_user, store, date)
            transaction_total += ((float(i[1]) * float(i[5])) * int(i[2])) if i[4] else (float(i[1]) * int(i[2]))
        self.DBM.push_transaction_summary(self.active_user, store, date, transaction_total)
        self.DBM.save()
        self.transaction_dict.clear()
        self.name_list = self.DBM.get_product_name_list()
        self.item_entry.lista = self.name_list
        self.transaction_box.clear()


