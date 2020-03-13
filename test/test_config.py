import unittest

from apps.Config.config import Config

class TestConfig(unittest.TestCase):

    def test_config_get(self):
        test_config = Config()

        port = test_config.get("groundstation","port")
    
        self.assertEqual(port, "24002")


if __name__ == '__main__':
    unittest.main()
