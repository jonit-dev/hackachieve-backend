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
            'mailgun_sandbox_login': os.environ.get('MAILGUN_SANDBOX_LOGIN'),
            'mailgun_sandbox_password': os.environ.get('MAILGUN_SANDBOX_PASSWORD'),
            'turn_off_transactional_emails_on_dev': os.environ.get('TURN_OFF_TRANSACTIONAL_EMAILS_ON_DEV'),
            'support_email': os.environ.get('SUPPORT_EMAIL'),
            'sendgrid_login': os.environ.get('SENDGRID_LOGIN'),
            'sendgrid_password': os.environ.get('SENDGRID_PASSWORD'),
            'postmark_login': os.environ.get('POSTMARK_LOGIN'),
            'postmark_password': os.environ.get('POSTMARK_PASSWORD'),
            'mailchimp_api_key': os.environ.get('MAILCHIMP_API_KEY'),
        }

        return keys[key]
