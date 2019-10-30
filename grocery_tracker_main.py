from tkinter import Tk
import gui_initiation
import database_management as DBM


def main():
    root = Tk()
    database_manager = DBM.DatabaseManager('example.db')
    main_gui = gui_initiation.MainGUI(root, database_manager)
    root.mainloop()


main()
