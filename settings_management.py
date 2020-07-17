import configparser


class SettingsManager:
    def __init__(self, settings_file):
        self.setting_file = settings_file
        self.config = configparser.ConfigParser()
        self.config.read(settings_file)
        if not self.config.has_section('main'):
            self.config.add_section('main')
            self.config.set('main', 'activeuser', 'Unidentified User')
            self.config.set('main', 'backgroundcolor', 'Red')
            with open(self.setting_file, 'w') as f:
                self.config.write(f)
        self.color_dict = {
            'Red': '#d63031', 'Blue': '#0984e3', 'Green': '#00b894', 'Black': '#2d3436',
            'Grey': '#636e72', 'Orange': '#e17055', 'Pink': '#fd79a8', 'Purple': '#6c5ce7',
            'Cyan': '#00cec9'}
        self.active_user = self.config.get('main', 'activeuser')
        self.background_color = self.config.get('main', 'backgroundcolor')

    def set_active_user(self, active_user):
        self.config.set('main', 'activeuser', active_user)
        with open(self.setting_file, 'w') as f:
            self.config.write(f)
        self.active_user = active_user

    def set_background_color(self, background_color):
        self.config.set('main', 'backgroundcolor', background_color)
        with open(self.setting_file, 'w') as f:
            self.config.write(f)
        self.background_color = background_color
