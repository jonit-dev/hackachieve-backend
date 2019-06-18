import os


class Environment:

    @staticmethod
    def getkey(key):
        keys = {
            "env": os.environ.get('ENV'),
            'mailgun_login': os.environ.get('MAILGUN_LOGIN'),
            'mailgun_password': os.environ.get('MAILGUN_PASSWORD'),
            'mailgun_sandbox_login': os.environ.get('MAILGUN_SANDBOX_LOGIN'),
            'mailgun_sandbox_password': os.environ.get('MAILGUN_SANDBOX_PASSWORD'),
            'send_transactional_emails': os.environ.get('SEND_TRANSACTIONAL_EMAILS'),
            'support_email': os.environ.get('SUPPORT_EMAIL'),
            'mailchimp_api_key': os.environ.get('MAILCHIMP_API_KEY'),
        }

        return keys[key]
