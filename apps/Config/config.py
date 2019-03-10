import configparser
import os

class Config:
    
    def __init__(self):
        self.config = self.get_config()
        self.groundstation_ip = self.config['groundstation']['ip'] 
        self.groundstation_port = self.config['groundstation']['port']
        self.obc_port = self.config['obc']['port']
        self.print_config()

    def get_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config

    def print_config(self):
        print('Configuration:' \
            '\n  OBC PORT: {0}'\
            '\n  GCS IP: {1}'\
            '\n  GCS PORT: {2}'.format(self.obc_port, self.groundstation_ip, self.groundstation_port))
config = Config()
