from tkinter import *
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
        self.mainframe = Frame(self.master, height=1200, width=800, bg='#4b130c')
        self.mainframe.grid(row=0, column=0, rowspan=10, columnspan=10, sticky=W + E + N + S, padx=0, pady=0)
        self.scrape_button = Button(self.mainframe, text="Settings", command=self.greet)
        self.scrape_button.grid(row=0, column=0, sticky=W, padx=(10, 0), pady=(10, 5))
        self.block_button = Button(self.mainframe, text="Block", command=self.greet)
        self.block_button.grid(row=1, column=0, sticky=W, padx=0, pady=(10, 5))
        self.include_button = Button(self.mainframe, text="Include", command=self.greet)
        self.include_button.grid(row=1, column=1, sticky=W, padx=0, pady=(10, 5))
        self.log_button = Button(self.mainframe, text="Log", command=self.greet)
        self.log_button.grid(row=1, column=2, sticky=W, padx=0, pady=(10, 5))
        self.settings_button = Button(self.mainframe, text="Settings", command=self.greet)
        self.settings_button.grid(row=1, column=3, sticky=W, padx=0, pady=(10, 5))
        self.entry = autocomplete_entry_widget.AutocompleteEntry(lista, self.master)
        self.entry.grid(row=0, column=2)

        self.transaction_box = sortable_table.Multicolumn_Listbox(self.mainframe, ["Item", "Price", "Category"], stripped_rows=("white", "#f2f2f2"), height=16, cell_anchor="center")
        self.transaction_box.interior.column(0, width=400)
        self.transaction_box.interior.column(1, width=200)
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