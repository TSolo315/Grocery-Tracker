from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import sortable_table
import autocomplete_entry_widget


lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket', 'brackets', 'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event',
         'events', 'example', 'field', 'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind', 'leave', 'left', 'like', 'manager', 'many', 'match',
         'modifier', 'most', 'of', 'or', 'others', 'out', 'part', 'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless', 'use', 'used', 'user',
         'various', 'ways', 'we', 'window', 'wish', 'you']


class MainGUI:
    def __init__(self, master, database_manager):
        self.master = master
        self.DBM = database_manager
        self.transaction_dict = {}

        master.title("Grocery Tracker")
        master.geometry("1200x800")
        main_background_color = '#4b130c'

        self.mainframe = Frame(self.master, height=1200, width=800, bg=main_background_color)
        self.mainframe.grid(row=0, column=0, rowspan=10, columnspan=20, sticky=W + E + N + S, padx=0, pady=0)
        self.item_label = Label(self.mainframe, text='Item:', bg=main_background_color)
        self.item_label.grid(row=1, column=0, sticky=W, padx=(10, 0), pady=(10, 5))
        self.item_entry = autocomplete_entry_widget.AutocompleteEntry(lista, self.mainframe)
        self.item_entry.grid(row=1, column=1, sticky=W, padx=(0, 0), pady=(10, 5))
        self.price_label = Label(self.mainframe, text='Price:', bg=main_background_color)
        self.price_label.grid(row=1, column=2, sticky=W, padx=(0, 0), pady=(10, 5))
        self.price_entry = Entry(self.mainframe)
        self.price_entry.grid(row=1, column=3, sticky=W, padx=(0, 0), pady=(10, 5))
        self.quantity_label = Label(self.mainframe, text='Quantity:', bg=main_background_color)
        self.quantity_label.grid(row=1, column=4, sticky=W, padx=(0, 0), pady=(10, 5))
        self.quantity_entry = Entry(self.mainframe)
        self.quantity_entry.grid(row=1, column=5, sticky=W, padx=(0, 0), pady=(10, 5))
        self.quantity_entry.insert(0, '1')
        self.weight_label = Label(self.mainframe, text='Weight (lb):', bg=main_background_color)
        self.weight_label.grid(row=1, column=6, sticky=W, padx=(0, 0), pady=(10, 5))
        self.weight_entry = Entry(self.mainframe)
        self.weight_entry.grid(row=1, column=7, sticky=W, padx=(0, 0), pady=(10, 5))
        self.category_label = Label(self.mainframe, text='Category:', bg=main_background_color)
        self.category_label.grid(row=1, column=8, sticky=W, padx=(0, 0), pady=(10, 5))
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
        self.transaction_box.interior.grid(row=2, rowspan=8, column=0, columnspan=10, sticky=W + N + S + E, padx=5, pady=5)

        self.store_label = Label(self.mainframe, text='Store:', bg=main_background_color)
        self.store_label.grid(row=10, column=0, sticky=W, padx=(0, 0), pady=(10, 10))
        self.store_box = Combobox(self.mainframe, textvariable='transaction_store', state="readonly")
        self.store_box['values'] = ('0.5 seconds', '1 seconds', '2 seconds', '3 seconds', '4 seconds', '5 seconds', '10 seconds', '20 seconds', '30 seconds', '60 seconds')
        self.store_box.current(0)
        self.store_box.grid(row=10, column=1, columnspan=1, sticky=W, padx=0, pady=(10, 10))
        self.transaction_submit_button = Button(self.mainframe, text="Submit Transaction", command=self.submit_item_entry)
        self.transaction_submit_button.grid(row=10, column=2, sticky=W, padx=0, pady=(10, 10))

        for i in range(0, 20):
            master.grid_columnconfigure(i, weight=1)
            self.mainframe.grid_columnconfigure(i, weight=1)
        for i in range(0, 10):
            master.grid_rowconfigure(i, weight=1)
            self.mainframe.grid_rowconfigure(i, weight=1)

        master.update()

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
        if not self.valid_number_test(item_weight, entry_name='Weight entry'):
            return
        # if item_quantity:
        #     item_price = str(round(float(item_price) / float(item_quantity), 2))
        if item_weight:
            item_price = '$' + str(round(float(item_price) / float(item_weight), 2)) + '/lb'
        else:
            item_price = "$" + item_price
        item_category = self.category_box.get()
        self.transaction_box.clear()
        self.transaction_dict.setdefault(item_name, [item_price, item_quantity, item_category])
        self.fill_transaction_box(self.transaction_dict)
        self.item_entry.delete(0, END)
        self.price_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.quantity_entry.insert(0, '1')
        self.weight_entry.delete(0, END)
        self.category_box.current(0)

