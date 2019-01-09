import os


class Environment:

    @staticmethod
    def getkey(key):
        keys = {
            "walkscore": os.environ.get('WALKSCORE_KEY'),
            "whitepages": os.environ.get('WHITEPAGES_KEY'),
            "ipstack": os.environ.get("IPSTACK_KEY"),
            "env": os.environ.get('ENV'),
            'mailgun_login': os.environ.get('MAILGUN_LOGIN'),
            'mailgun_password': os.environ.get('MAILGUN_PASSWORD'),
            'support_email': os.environ.get('SUPPORT_EMAIL'),
            'sendgrid_login': os.environ.get('SENDGRID_LOGIN'),
            'sendgrid_password': os.environ.get('SENDGRID_PASSWORD'),
            'postmark_login': os.environ.get('POSTMARK_LOGIN'),
            'postmark_password': os.environ.get('POSTMARK_PASSWORD'),
        }

        return keys[key]
