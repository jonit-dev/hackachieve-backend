import os


class Environment:

    @staticmethod
    def getkey(key):
        keys = {
            "walkscore": os.environ.get('WALKSCORE_KEY'),
            "env": os.environ.get('ENV'),
            'mailgun_login': os.environ.get('MAILGUN_LOGIN'),
            'mailgun_password': os.environ.get('MAILGUN_PASSWORD'),
        }

        return keys[key]
