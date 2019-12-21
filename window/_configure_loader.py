import configparser


class ConfigureLoader:
    window_width = window_height = None
    window_minimum_width = window_minimum_height = None

    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.filename = 'settings.ini'
        self.read_data()

    def read_data(self):
        self.cf.read(self.filename)
        self.window_width = int(self.cf.get('window', 'width'))
        self.window_height = int(self.cf.get('window', 'height'))
        self.window_minimum_width = int(self.cf.get('window_const', 'minimum_width'))
        self.window_minimum_height = int(self.cf.get('window_const', 'minimum_height'))

    def write_data(self):
        # self.cf.add_section('window')
        self.cf.set('window', 'width', str(self.window_width))
        self.cf.set('window', 'height', str(self.window_height))
        with open(self.filename, 'w+') as f:
            self.cf.write(f)
