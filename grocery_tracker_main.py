from tkinter import Tk
import gui_initiation
import settings_management
import database_management


def main():
    root = Tk()
    settings_manager = settings_management.SettingsManager('settings.ini')
    database_manager = database_management.DatabaseManager('grocery_tracker.db')
    main_gui = gui_initiation.MainGUI(root, settings_manager, database_manager)
    root.mainloop()


if __name__ == '__main__':
    main()
