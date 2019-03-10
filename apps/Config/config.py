import configparser

class Config:
    
    def __init__(self):
        self.values = self.get_values()
        self.groundstation_ip = self.values['groundstation']['ip'] 
        self.groundstation_port = self.values['groundstation']['port']
        self.obc_port = self.values['obc']['port']
        self.print_values()

    def get_values(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    def print_values(self):
        print('Configuration:' \
            '\n  OBC PORT: {0}'\
            '\n  GCS IP: {1}'\
            '\n  GCS PORT: {2}'.format(self.obc_port, self.groundstation_ip, self.groundstation_port))
config = Config()
