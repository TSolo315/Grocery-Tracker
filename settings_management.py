import configparser


class SettingsManager:
    def __init__(self, settings_file):
        self.config = configparser.ConfigParser()
        self.config.read(settings_file)
        self.active_user = self.config.get('main', 'activeuser')
