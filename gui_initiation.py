from tkinter import *
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

        master.title("Grocery Tracker")
        master.geometry("1200x800")
        main_background_color = '#4b130c'
        self.mainframe = Frame(self.master, height=1200, width=800, bg=main_background_color)
        self.mainframe.grid(row=0, column=0, rowspan=10, columnspan=10, sticky=W + E + N + S, padx=0, pady=0)
        self.item_label = Label(self.mainframe, text='Item:', bg=main_background_color)
        self.item_label.grid(row=1, column=0, sticky=W, padx=(10, 0), pady=(10, 5))
        self.item_entry = autocomplete_entry_widget.AutocompleteEntry(lista, self.mainframe)
        self.item_entry.grid(row=1, column=1)
        self.price_label = Label(self.mainframe, text='Price:', bg=main_background_color)
        self.price_label.grid(row=1, column=2, sticky=W, padx=(0, 0), pady=(10, 5))
        self.price_entry = Entry(self.mainframe)
        self.price_entry.grid(row=1, column=3, sticky=W, padx=(0, 0), pady=(10, 5))
        self.weight_label = Label(self.mainframe, text='Weight (lb):', bg=main_background_color)
        self.weight_label.grid(row=1, column=4, sticky=W, padx=(0, 0), pady=(10, 5))
        self.weight_entry = Entry(self.mainframe)
        self.weight_entry.grid(row=1, column=5, sticky=W, padx=(0, 0), pady=(10, 5))
        self.category_label = Label(self.mainframe, text='Category:', bg=main_background_color)
        self.category_label.grid(row=1, column=6, sticky=W, padx=(0, 0), pady=(10, 5))
        self.category_box = Combobox(self.mainframe, textvariable='item_category', state="readonly")
        self.category_box['values'] = ('0.5 seconds', '1 seconds', '2 seconds', '3 seconds', '4 seconds', '5 seconds', '10 seconds', '20 seconds', '30 seconds', '60 seconds')
        self.category_box.grid(row=1, column=7, columnspan=2, sticky=W, padx=0, pady=(10, 5))
        self.transaction_box = sortable_table.Multicolumn_Listbox(self.mainframe, ["Item", "Price", "Category"], stripped_rows=("white", "#f2f2f2"), height=16, cell_anchor="center")
        self.transaction_box.interior.column(0, width=300)
        self.transaction_box.interior.column(1, width=150)
        self.transaction_box.interior.column(2, width=200)
        self.transaction_box.interior.grid(row=2, rowspan=9, column=0, columnspan=9, sticky=W + N + S + E, padx=5, pady=5)

        for i in range(0, 10):
            master.grid_columnconfigure(i, weight=1)
            self.mainframe.grid_columnconfigure(i, weight=1)
            master.grid_rowconfigure(i, weight=1)
            self.mainframe.grid_rowconfigure(i, weight=1)

        master.update()

    def greet(self):
        print("Greetings!")