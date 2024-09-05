import os
import time
import unittest
import yaml
from proxytg.telegram import TelegramAccount


class TestTelegramAccount(unittest.TestCase):

    def test_login(self):
        print(os.getcwd())
        cfg = yaml.safe_load(open('config.yml'))
        for root, dirs, files in os.walk(cfg['sessions_dir'], topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)

            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)

        os.rmdir(cfg['sessions_dir'])
        obj = TelegramAccount("account", cfg['proxy'], cfg['sessions_dir'])
        time.sleep(2)
        self.assertRegex(obj.driver.current_url, r"https://web.telegram.org/.*")


if __name__ == '__main__':
    unittest.main()
