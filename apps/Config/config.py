import configparser


class Config:
    def __init__(self):
        self.values = self.get_values()
        self.print_values()

    def get_values(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        return config

    def print_values(self):
        print(
            "Configuration:"
            "\n  OBC PORT: {0}"
            "\n  GCS IP: {1}"
            "\n  GCS PORT: {2}".format(
                self.values["obc"]["port"],
                self.values["groundstation"]["ip"],
                self.values["groundstation"]["port"],
            )
        )


config = Config()
