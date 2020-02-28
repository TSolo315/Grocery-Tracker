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

        self.transaction_dict = {}
        self.today_date = datetime.today().strftime("%Y-%m-%d")

        self.category_list = ["Alcoholic Beverages", "Baby Foods", "Beverages", "Breads & Bakery", "Breakfast Foods",
                              "Candy & Chocolate", "Dairy, Cheese & Eggs", "Deli & Prepared Foods", "Dessert", "Food & Beverage Gifts",
                              "Fresh Flowers", "Frozen Foods", "Meat & Seafood", "Meat Substitutes", "Pantry Staples", "Produce", "Snack Foods",
                              "Arts & Crafts", "Automotive", "Beauty", "Clothing & Accessories", "Electronics", "Health", "Home", "Home Improvement",
                              "Office", "Outdoors", "Personal Care", "Pets", "Sports", "Toys", "Video Games", "Miscellaneous"]
        self.name_list = []
        self.name_dict = self.DBM.get_product_name_list()
        for i in self.name_dict:
            self.name_list.append(i)
        self.store_list = self.DBM.get_store_list()
        self.username_list = self.DBM.get_user_list()

        self.active_user = self.SM.active_user
        self.background_color = self.SM.background_color
        self.main_background_color = self.SM.color_dict[self.background_color]
        self.main_foreground_color = '#FFFAFA'

        master.title("Grocery Tracker: " + self.active_user)
        master.geometry("1200x800")

        self.mainframe = Frame(self.master, height=1200, width=800, bg=self.main_background_color)
        self.mainframe.grid(row=0, column=0, rowspan=10, columnspan=12, sticky=W + E + N + S, padx=0, pady=0)
        self.top_button_frame = Frame(self.mainframe, bg=self.main_background_color)
        self.top_button_frame.grid(row=0, column=0, rowspan=2, columnspan=12, sticky=W + E + N + S, padx=0, pady=0)
        self.settings_button = Button(self.top_button_frame, text="Settings", font="helvetica", command=self.open_settings_menu)
        self.settings_button.grid(row=0, column=0, columnspan=2, sticky=W, padx=(20, 5), pady=(20, 0))
        self.report_button = Button(self.top_button_frame, text="Get Report", font="helvetica", command=self.open_report_menu)
        self.report_button.grid(row=0, column=2, columnspan=2, sticky=W, padx=(10, 10), pady=(20, 0))
        self.item_label = Label(self.mainframe, text='Item:', bg=self.main_background_color, fg=self.main_foreground_color)
        self.item_label.grid(row=1, column=0, sticky=W, padx=(20, 0), pady=(5, 5))
        self.item_entry = autocomplete_entry_widget.AutocompleteEntry(self.name_list, self.mainframe)
        self.item_entry.grid(row=1, column=1, sticky=W, padx=(0, 0), pady=(5, 5))
        self.item_entry.bind('<FocusOut>', self.set_item_category)
        self.price_label = Label(self.mainframe, text='Price:', bg=self.main_background_color, fg=self.main_foreground_color)
        self.price_label.grid(row=1, column=2, sticky=W, padx=(0, 0), pady=(5, 5))
        self.price_entry = Entry(self.mainframe)
        self.price_entry.grid(row=1, column=3, sticky=W, padx=(0, 0), pady=(5, 5))
        self.quantity_label = Label(self.mainframe, text='Quantity:', bg=self.main_background_color, fg=self.main_foreground_color)
        self.quantity_label.grid(row=1, column=4, sticky=W, padx=(0, 0), pady=(5, 5))
        self.quantity_entry = Entry(self.mainframe)
        self.quantity_entry.grid(row=1, column=5, sticky=W, padx=(0, 0), pady=(5, 5))
        self.quantity_entry.insert(0, '1')
        self.weight_label = Label(self.mainframe, text='Weight (lb):', bg=self.main_background_color, fg=self.main_foreground_color)
        self.weight_label.grid(row=1, column=6, sticky=W, padx=(0, 0), pady=(5, 5))
        self.weight_entry = Entry(self.mainframe)
        self.weight_entry.grid(row=1, column=7, sticky=W, padx=(0, 0), pady=(5, 5))
        self.category_label = Label(self.mainframe, text='Category:', bg=self.main_background_color, fg=self.main_foreground_color)
        self.category_label.grid(row=1, column=8, sticky=W, padx=(0, 0), pady=(5, 5))
        self.category_box = Combobox(self.mainframe, textvariable='item_category', state="readonly", width=22)
        self.category_box['values'] = self.category_list
        self.category_box.current(0)
        self.category_box.grid(row=1, column=9, columnspan=1, sticky=W, padx=0, pady=(10, 5))
        self.item_submit_button = Button(self.mainframe, text="Submit", command=self.submit_item_entry)
        self.item_submit_button.grid(row=1, column=10, sticky=W, padx=0, pady=(10, 5))

        self.transaction_box = sortable_table.Multicolumn_Listbox(self.mainframe, ["Item", "Price", "Quantity", "Category"], stripped_rows=("white", "#f2f2f2"), height=16, cell_anchor="center")
        self.transaction_box.interior.column(0, width=250)
        self.transaction_box.interior.column(1, width=100)
        self.transaction_box.interior.column(2, width=50)
        self.transaction_box.interior.column(3, width=150)
        self.transaction_box.interior.grid(row=2, rowspan=8, column=0, columnspan=10, sticky=W + N + S + E, padx=(20, 5), pady=5)

        self.store_label = Label(self.mainframe, text='Store:', bg=self.main_background_color, fg=self.main_foreground_color)
        self.store_label.grid(row=10, column=0, sticky=W, padx=(20, 0), pady=(10, 10))
        self.store_box = Combobox(self.mainframe, textvariable='transaction_store', state="readonly")
        if len(self.store_list):
            self.store_box['values'] = self.store_list
        else:
            self.store_box['values'] = ['No Stores Added']
        self.store_box.current(0)
        self.store_box.grid(row=10, column=1, sticky=W, padx=0, pady=(10, 20))
        self.date_label = Label(self.mainframe, text='Date:', bg=self.main_background_color, fg=self.main_foreground_color)
        self.date_label.grid(row=10, column=2, sticky=W, padx=(10, 0), pady=(10, 20))
        self.date_entry = Entry(self.mainframe)
        self.date_entry.grid(row=10, column=3, sticky=W, padx=(0, 0), pady=(10, 20))
        self.date_entry.insert(0, self.today_date)
        self.transaction_submit_button = Button(self.mainframe, text="Submit Transaction", command=self.submit_transaction)
        self.transaction_submit_button.grid(row=10, column=9, sticky=E, padx=(0, 5), pady=(10, 20))

        for i in range(0, 12):
            master.grid_columnconfigure(i, weight=1)
            self.mainframe.grid_columnconfigure(i, weight=1)
        for i in range(0, 10):
            master.grid_rowconfigure(i, weight=1)
            self.mainframe.grid_rowconfigure(i, weight=1)

        try:
            self.master.iconbitmap('GTicon.ico')
        except TclError:
            pass

        master.update()
        if not len(self.name_list) and self.active_user == "Unidentified User":
            self.master.after(1000, self.new_user_alert)

    def new_user_alert(self):
        messagebox.showinfo("Hello!", "It looks like this might be your first time here. Please start by going into the settings menu and adding a new user and new store.")

    def set_item_category(self, event):
        if self.item_entry.get() in self.name_dict:
            self.category_box.current(self.category_list.index(self.name_dict[self.item_entry.get()][0]))

    def change_background_color(self, color):
        self.mainframe.config(bg=color)
        self.top_button_frame.config(bg=color)
        self.item_label.config(bg=color)
        self.price_label.config(bg=color)
        self.quantity_label.config(bg=color)
        self.weight_label.config(bg=color)
        self.category_label.config(bg=color)
        self.store_label.config(bg=color)
        self.date_label.config(bg=color)

    def open_settings_menu(self):

        def add_user_menu():

            def add_new_user():
                new_username = username_entry.get()
                if not new_username:
                    self.error_alert("Username is already taken.")
                    return
                self.DBM.push_new_user(new_username)
                self.DBM.save()
                self.username_list.append(new_username)
                if username_box:
                    username_box['values'] = self.username_list
                    username_box.current(len(self.username_list) - 1)
                self.SM.set_active_user(new_username)
                self.active_user = self.SM.active_user
                self.master.title("Grocery Tracker: " + self.active_user)
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

            def add_new_store():
                store_name = store_name_entry.get()
                if not store_name:
                    self.error_alert("Please enter a store name.")
                    return
                store_address = store_address_entry.get()
                if not store_address:
                    self.error_alert("Please enter a store address.")
                    return
                store_address2 = store_address_entry2.get()
                store_city = store_city_entry.get()
                if not store_city:
                    self.error_alert("Please enter a city.")
                    return
                store_state = store_state_entry.get()
                if not store_state:
                    self.error_alert("Please enter a state.")
                    return
                store_zip = store_zip_entry.get()
                if not store_zip:
                    self.error_alert("Please enter a zip code.")
                    return
                self.DBM.push_new_store(store_name, store_address, store_address2, store_city, store_state, store_zip)
                self.DBM.save()
                self.store_list.append(store_name + " - " + store_city)
                self.store_box['values'] = self.store_list
                as_menu.destroy()
                self.store_box.current(0)
                messagebox.showinfo("Success", "New Store Added!")

            def close_new_store_menu():
                as_menu.destroy()

            xx = self.master.winfo_x()
            yy = self.master.winfo_y()
            dxx = 30
            dyy = 30
            as_menu = Toplevel(height=400, width=400)
            as_menu.transient(settings_menu)
            as_menu.title("Add Store")
            as_menu.update()
            as_menu.geometry("+%d+%d" % (xx + dxx, yy + dyy))

            store_name_label = Label(as_menu, text='Store Name:')
            store_name_label.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
            store_name_entry = Entry(as_menu)
            store_name_entry.grid(row=0, column=1, sticky=W, padx=(5, 10), pady=(10, 0))
            store_address_label = Label(as_menu, text='Address:')
            store_address_label.grid(row=1, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
            store_address_entry = Entry(as_menu)
            store_address_entry.grid(row=1, column=1, sticky=W, padx=(5, 10), pady=(10, 0))
            store_address_label2 = Label(as_menu, text='Address2:')
            store_address_label2.grid(row=2, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
            store_address_entry2 = Entry(as_menu)
            store_address_entry2.grid(row=2, column=1, sticky=W, padx=(5, 10), pady=(10, 0))
            store_city_label = Label(as_menu, text='City:')
            store_city_label.grid(row=3, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
            store_city_entry = Entry(as_menu)
            store_city_entry.grid(row=3, column=1, sticky=W, padx=(5, 10), pady=(10, 0))
            store_state_label = Label(as_menu, text='State:')
            store_state_label.grid(row=4, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
            store_state_entry = Entry(as_menu)
            store_state_entry.grid(row=4, column=1, sticky=W, padx=(5, 10), pady=(10, 0))
            store_zip_label = Label(as_menu, text='Zip:')
            store_zip_label.grid(row=5, column=0, sticky=W, padx=(10, 5), pady=(10, 0))
            store_zip_entry = Entry(as_menu)
            store_zip_entry.grid(row=5, column=1, sticky=W, padx=(5, 10), pady=(10, 0))
            store_buttons_frame = Frame(as_menu)
            store_buttons_frame.grid(row=6, column=0, columnspan=2, sticky=W + E + N + S, padx=0, pady=0)
            add_new_store_button = Button(store_buttons_frame, text="Add Store", command=add_new_store)
            add_new_store_button.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=10)
            close_new_store_button = Button(store_buttons_frame, text="Close", command=close_new_store_menu)
            close_new_store_button.grid(row=0, column=1, sticky=W, padx=(5, 10), pady=10)

        def save_settings():
            username = username_box.get()
            if username == "Unidentified User":
                self.error_alert("Please add a new user before saving settings.")
                return
            background_color = background_color_box.get()
            if username != self.active_user:
                self.SM.set_active_user(username)
                self.active_user = self.SM.active_user
                self.master.title("Grocery Tracker: " + self.active_user)
            if background_color != self.background_color:
                self.SM.set_background_color(background_color)
                self.background_color = self.SM.background_color
                self.main_background_color = self.SM.color_dict[self.background_color]
                self.change_background_color(self.main_background_color)

        def close_settings_menu():
            settings_menu.destroy()

        color_list = ['Red', 'Blue', 'Black', 'Grey', 'Orange', 'Pink', 'Green', 'Purple', 'Cyan']
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
        if len(self.username_list):
            username_box['values'] = self.username_list
            try:
                username_box.current(self.username_list.index(self.active_user))
            except ValueError:
                username_box.current(0)
        else:
            username_box['values'] = ['Unidentified User']
            username_box.current(0)
        username_box.grid(row=0, column=1, sticky=W, padx=(0, 10), pady=(10, 10))
        background_color_label = Label(settings_menu, text='Background Color:')
        background_color_label.grid(row=1, column=0, sticky=W, padx=(10, 5), pady=(10, 10))
        background_color_box = Combobox(settings_menu, textvariable='bgcolor', state="readonly")
        background_color_box['values'] = color_list
        background_color_box.current(color_list.index(self.background_color))
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

    def open_report_menu(self):

        def close_report_menu():
            report_menu.destroy()

        def open_report_result_menu(report_data, query_summary, item_search):
            """report_data_indexes: 0:username_name, 1:product_name, 2:transaction_price, 3:product_lowest_price, 4:product_average_price, 5:product_highest_price, 6:product_times_purchased,
             7:product_category, 8:product_weight_based_price, 9:store_name, 10:transaction_quantity, 11:transaction_date, 12:transaction_weight"""
            if len(report_data) == 0:
                self.error_alert('No transactions match your query.')
                return
            xx = self.master.winfo_x()
            yy = self.master.winfo_y()
            ddx = 60
            ddy = 60
            report_result_menu = Toplevel(height=400, width=400)
            report_result_menu.transient(self.master)
            report_result_menu.title("Report")
            report_result_menu.update()
            report_result_menu.geometry("+%d+%d" % (xx + ddx, yy + ddy))

            report_title_label = Label(report_result_menu, text='Here is your Report:', font="Helvetica")
            report_title_label.grid(row=0, column=0, sticky=W, padx=(20, 5), pady=(10, 5))

            if not query_summary:
                column_names = ["Username", "Store", "Item", "Price", "Quantity", "Category", "Date"]
                report_box = sortable_table.Multicolumn_Listbox(report_result_menu, column_names, stripped_rows=("white", "#f2f2f2"), height=16, cell_anchor="center")
                report_box.interior.column(0, width=125)
                report_box.interior.column(1, width=175)
                report_box.interior.column(2, width=275)
                report_box.interior.column(3, width=100)
                report_box.interior.column(4, width=65)
                report_box.interior.column(5, width=150)
                report_box.interior.column(6, width=100)
                report_box.interior.grid(row=1, rowspan=8, column=0, columnspan=10, sticky=W + N + S + E, padx=20, pady=10)

                item_total = 0
                used_rows = 1
                category_dict = {}
                store_dict = {}

                for i in self.category_list:
                    category_dict.setdefault(i, 0)
                for i in self.store_list:
                    store_dict.setdefault(i.split(" - ")[0], 0)

                for i in report_data:
                    if i[8]:
                        if not i[12]:
                            product_weight = 1
                        else:
                            product_weight = i[12]
                        item_total += (i[2] * product_weight) * i[10]
                        category_dict[i[7]] += (i[2] * product_weight) * i[10]
                        store_dict[i[9]] += (i[2] * product_weight) * i[10]
                    else:
                        item_total += i[2] * i[10]
                        category_dict[i[7]] += i[2] * i[10]
                        store_dict[i[9]] += i[2] * i[10]
                    report_box.insert_row([i[0], i[9], i[1], '$' + str(i[2]) + '/lb' if i[8] else '$' + str(i[2]), i[10], i[7], i[11]])

                category_overview_label = Label(report_result_menu, text='Category Overview:', font="Helvetica")
                category_overview_label.grid(row=10, column=0, sticky=W, padx=(20, 0), pady=3)
                category_label_dict = {}
                for category, total in category_dict.items():
                    if total != 0:
                        category_label_dict.setdefault('category_label' + str(used_rows), Label(report_result_menu, text=category + ": $" + str(total)))
                        category_label_dict['category_label' + str(used_rows)].grid(row=int((used_rows / 4) + 10), column=used_rows % 4, sticky=W, padx=(20, 0), pady=3)
                        used_rows += 1

                store_overview_label = Label(report_result_menu, text='Store Overview:', font="Helvetica")
                store_overview_label.grid(row=int((used_rows / 4) + 11), column=0, sticky=W, padx=(20, 0), pady=3)
                store_label_dict = {}
                store_column = 1
                for store, total in store_dict.items():
                    if total != 0:
                        store_label_dict.setdefault('category_label' + str(used_rows), Label(report_result_menu, text=store + ": $" + str(total)))
                        store_label_dict['category_label' + str(used_rows)].grid(row=int((used_rows / 4) + 11), column=store_column, sticky=W, padx=(20, 0), pady=3)
                        used_rows += 1
                        if store_column >= 3:
                            store_column = 0
                        else:
                            store_column += 1

                total_overview_label = Label(report_result_menu, text='Total Spending: $' + str(item_total), font="Helvetica")
                total_overview_label.grid(row=int((used_rows / 4) + 12), column=0, sticky=W, padx=(20, 0), pady=3)

                if item_search:
                    item_highest_label = Label(report_result_menu, text='Item Highest Price: $' + str(report_data[0][5]) + '/lb' if report_data[0][8] else 'Item Highest Price: $' + str(report_data[0][5]), font="Helvetica")
                    item_highest_label.grid(row=int((used_rows / 4) + 13), column=0, sticky=W, padx=(20, 0), pady=3)
                    item_average_label = Label(report_result_menu, text='Item Average Price: $' + str(report_data[0][4]) + '/lb' if report_data[0][8] else 'Item Highest Price: $' + str(report_data[0][4]), font="Helvetica")
                    item_average_label.grid(row=int((used_rows / 4) + 14), column=0, sticky=W, padx=(20, 0), pady=3)
                    item_lowest_label = Label(report_result_menu, text='Item Lowest Price: $' + str(report_data[0][3]) + '/lb' if report_data[0][8] else 'Item Highest Price: $' + str(report_data[0][3]), font="Helvetica")
                    item_lowest_label.grid(row=int((used_rows / 4) + 15), column=0, sticky=W, padx=(20, 0), pady=3)
                    close_settings_button = Button(report_result_menu, text="Close", command=lambda: report_result_menu.destroy())
                    close_settings_button.grid(row=int((used_rows / 4) + 16), column=0, sticky=W, padx=(20, 0), pady=(5, 10))

                else:
                    close_settings_button = Button(report_result_menu, text="Close", command=lambda: report_result_menu.destroy())
                    close_settings_button.grid(row=int((used_rows / 4) + 13), column=0, sticky=W, padx=(20, 0), pady=(5, 10))
            else:
                column_names = ["Username", "Store", "Total", "Date"]
                report_box = sortable_table.Multicolumn_Listbox(report_result_menu, column_names, stripped_rows=("white", "#f2f2f2"), height=16, cell_anchor="center")
                report_box.interior.column(0, width=100)
                report_box.interior.column(1, width=200)
                report_box.interior.column(2, width=100)
                report_box.interior.column(3, width=100)
                report_box.interior.grid(row=1, rowspan=8, column=0, columnspan=4, sticky=W + N + S + E, padx=20, pady=10)

                item_total = 0
                used_rows = 1
                store_dict = {}

                for i in self.store_list:
                    store_dict.setdefault(i.split(" - ")[0], 0)

                for i in report_data:
                    item_total += i[3]
                    store_dict[i[1]] += i[3]
                    report_box.insert_row([i[0], i[1], '$' + str(i[3]), i[2]])

                store_overview_label = Label(report_result_menu, text='Store Overview:', font="Helvetica")
                store_overview_label.grid(row=10, column=0, sticky=W, padx=(20, 0), pady=3)
                store_label_dict = {}
                for category, total in store_dict.items():
                    if total != 0:
                        store_label_dict.setdefault('store_label' + str(used_rows), Label(report_result_menu, text=category + ": $" + str(total)))
                        store_label_dict['store_label' + str(used_rows)].grid(row=int((used_rows / 3) + 10), column=used_rows % 3, sticky=W, padx=(20, 0), pady=3)
                        used_rows += 1

                total_overview_label = Label(report_result_menu, text='Total Spending: $' + str(item_total), font="Helvetica")
                total_overview_label.grid(row=int((used_rows / 3) + 11), column=0, sticky=W, padx=(20, 0), pady=3)

                close_settings_button = Button(report_result_menu, text="Close", command=lambda: report_result_menu.destroy())
                close_settings_button.grid(row=int((used_rows / 3) + 12), column=0, sticky=W, padx=(20, 0), pady=(5, 10))

        def submit_query():
            item_search = False
            query_user = report_username_box.get()
            query_store = report_store_box.get()
            query_item = report_item_entry.get()
            if query_item:
                item_search = True
                if query_item not in self.name_list:
                    self.error_alert('Item not found, please double check spelling.')
                    return
            query_category = report_category_box.get()
            query_date1 = report_date_entry1.get()
            if query_date1 and not self.validate_date_format(query_date1):
                return
            query_date2 = report_date_entry2.get()
            if query_date2 and not self.validate_date_format(query_date2):
                return
            query_summary = summary_report_var.get()
            open_report_result_menu(self.DBM.retrieve_report_query(query_user, query_store, query_item, query_category, query_date1, query_date2, query_summary), query_summary, item_search)

        x = self.master.winfo_x()
        y = self.master.winfo_y()
        dx = 60
        dy = 60
        report_menu = Toplevel(height=400, width=400)
        report_menu.transient(self.master)
        report_menu.title("Generate Report")
        report_menu.update()
        report_menu.geometry("+%d+%d" % (x + dx, y + dy))

        report_username_list = self.username_list.copy()
        report_username_list.append('All Users')
        report_store_list = ["All Stores"] + self.store_list.copy()
        report_category_list = ["All Categories"] + self.category_list.copy()

        report_userbox_label = Label(report_menu, text='User:')
        report_userbox_label.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=(15, 10))
        report_username_box = Combobox(report_menu, textvariable='username', state="readonly", width=22)
        report_username_box['values'] = report_username_list
        report_username_box.current(self.username_list.index(self.active_user))
        report_username_box.grid(row=0, column=1, sticky=W, padx=(0, 10), pady=(15, 10))
        report_storebox_label = Label(report_menu, text='Store:')
        report_storebox_label.grid(row=0, column=2, sticky=W, padx=(5, 5), pady=(15, 10))
        report_store_box = Combobox(report_menu, textvariable='storename', state="readonly", width=22)
        report_store_box['values'] = report_store_list
        report_store_box.current(0)
        report_store_box.grid(row=0, column=3, sticky=W, padx=(0, 10), pady=(15, 10))
        report_item_label = Label(report_menu, text='Item:')
        report_item_label.grid(row=1, column=0, sticky=W, padx=(10, 5), pady=(10, 10))
        report_item_entry = autocomplete_entry_widget.AutocompleteEntry(self.name_list, report_menu, width=25)
        report_item_entry.grid(row=1, column=1, sticky=W, padx=(0, 10), pady=(10, 10))
        report_category_label = Label(report_menu, text='Category:')
        report_category_label.grid(row=1, column=2, sticky=W, padx=(5, 5), pady=(10, 10))
        report_category_box = Combobox(report_menu, textvariable='report_item_category', state="readonly", width=22)
        report_category_box['values'] = report_category_list
        report_category_box.current(0)
        report_category_box.grid(row=1, column=3, sticky=W, padx=(0, 10), pady=(10, 10))
        report_date_label1 = Label(report_menu, text='Date:')
        report_date_label1.grid(row=2, column=0, sticky=W, padx=(10, 5), pady=(10, 10))
        report_date_entry1 = Entry(report_menu, width=25)
        report_date_entry1.grid(row=2, column=1, sticky=W, padx=(0, 10), pady=(10, 10))
        report_date_label2 = Label(report_menu, text='to')
        report_date_label2.grid(row=2, column=2, sticky=W, padx=(10, 5), pady=(10, 10))
        report_date_entry2 = Entry(report_menu, width=25)
        report_date_entry2.grid(row=2, column=3, sticky=W, padx=(0, 10), pady=(10, 10))
        report_check_frame = Frame(report_menu)
        report_check_frame.grid(row=3, column=0, columnspan=4, sticky=W + E, padx=0, pady=0)
        summary_report_var = IntVar()
        summary_report_check = Checkbutton(report_check_frame, text="Transaction Summary Report", variable=summary_report_var)
        summary_report_check.grid(row=3, column=0, sticky=W, padx=(10, 5), pady=5)
        report_instruction_frame = Frame(report_menu)
        report_instruction_frame.grid(row=4, column=0, columnspan=4, sticky=W + E, padx=0, pady=(3, 0))
        report_instruction_label = Label(report_instruction_frame, text='Instructions:', font=("Helvetica", 18))
        report_instruction_label.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=0)
        report_instruction_label2 = Label(report_instruction_frame, text='• Form a query using the fields above.', font=("Helvetica", 11))
        report_instruction_label2.grid(row=1, column=0, sticky=W, padx=(18, 5), pady=5)
        report_instruction_label3 = Label(report_instruction_frame, text='• Leave unnecessary fields blank.', font=("Helvetica", 11))
        report_instruction_label3.grid(row=2, column=0, sticky=W, padx=(18, 5), pady=5)
        report_instruction_label3 = Label(report_instruction_frame, text='• Use date format YYYY-MM-DD.', font=("Helvetica", 11))
        report_instruction_label3.grid(row=3, column=0, sticky=W, padx=(18, 5), pady=5)
        report_instruction_label4 = Label(report_instruction_frame, text='• You can enter only one date.', font=("Helvetica", 11))
        report_instruction_label4.grid(row=4, column=0, sticky=W, padx=(18, 5), pady=5)
        report_instruction_label5 = Label(report_instruction_frame, text='• Transaction Summary Reports only show transaction totals.', font=("Helvetica", 11))
        report_instruction_label5.grid(row=5, column=0, sticky=W, padx=(18, 5), pady=5)
        report_button_frame = Frame(report_menu)
        report_button_frame.grid(row=5, column=0, columnspan=4, sticky=W + E, padx=0, pady=(3, 0))
        submit_query_button = Button(report_button_frame, text="Get Report", command=submit_query)
        submit_query_button.grid(row=0, column=0, sticky=W, padx=(10, 5), pady=(5, 10))
        close_report_button = Button(report_button_frame, text="Close", command=close_report_menu)
        close_report_button.grid(row=0, column=1, sticky=W, padx=(5, 10), pady=(5, 10))

    def error_alert(self, message):
        messagebox.showinfo("Error", message)

    def valid_number_test(self, source_input, is_float=True, entry_name='Entry'):
        if is_float:
            try:
                testvar = float(source_input)
            except ValueError:
                self.error_alert(entry_name + ' does not contain a valid number!')
                return False
        else:
            try:
                testvar = int(source_input)
            except ValueError:
                self.error_alert(entry_name + ' does not contain a valid number!')
                return False
        return True

    def validate_date_format(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            self.error_alert("Incorrect date format, should be YYYY-MM-DD")
            return False

    def fill_transaction_box(self, transaction_dict):
        transaction_list = []
        for key, value in transaction_dict.items():
            group_listing = [key]
            group_listing.extend(value)
            transaction_list.append(group_listing)
        for i in transaction_list:
            self.transaction_box.insert_row([i[0], i[1], i[2], i[3]])

    def submit_item_entry(self):
        item_name = self.item_entry.get().lower()
        if not item_name:
            self.error_alert('Please insert an item name.')
            return
        item_price = self.price_entry.get().replace("$", "")
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
        if item_name in self.name_dict:
            if not item_weight or item_weight == '0':
                if self.name_dict[item_name][1]:
                    self.error_alert('Please set a weight for this item as you have done previously.')
                    return
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
            self.error_alert('Empty Transaction')
            return
        store = self.store_box.get()
        if store == "No Stores Added":
            self.error_alert("Please add a store in the settings menu before submitting a transaction.")
            return
        date = self.date_entry.get()
        if not self.validate_date_format(date):
            return
        if self.active_user == "Unidentified User":
            self.error_alert("Please add a new user in the settings menu before submitting a transaction.")
            return
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
        messagebox.showinfo("Success", "Transaction Recorded!")


