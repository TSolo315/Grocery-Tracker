from tkinter import *
import re


class AutocompleteEntry(Entry):
    def __init__(self, lista, master, name_dict=0, cat_list=0, cat_box=0, *args, **kwargs):

        Entry.__init__(self, master, *args, **kwargs)
        self.lista = lista
        self.master = master
        self.name_dict = name_dict
        self.cat_list = cat_list
        self.cat_box = cat_box
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Tab>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            if hasattr(self, 'lb'):
                self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox(self.master)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END, w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def set_item_category(self, active):
        if active in self.name_dict:
            self.cat_box.current(self.cat_list.index(self.name_dict[active][0]))

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            if self.cat_box:
                self.set_item_category(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + self.var.get().lower() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]
