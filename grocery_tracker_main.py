from tkinter import Tk
import gui_initiation
import database_management


def main():
    root = Tk()
    database_manager = database_management.DatabaseManager('grocery_tracker.db')
    main_gui = gui_initiation.MainGUI(root, database_manager)
    root.mainloop()


if __name__ == '__main__':
    main()
