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
            'send_transactional_emails': os.environ.get('SEND_TRANSACTIONAL_EMAILS'),
            'support_email': os.environ.get('SUPPORT_EMAIL'),
            'sendgrid_login': os.environ.get('SENDGRID_LOGIN'),
            'sendgrid_password': os.environ.get('SENDGRID_PASSWORD'),
            'postmark_login': os.environ.get('POSTMARK_LOGIN'),
            'postmark_password': os.environ.get('POSTMARK_PASSWORD'),
            'mailchimp_api_key': os.environ.get('MAILCHIMP_API_KEY'),
        }

        return keys[key]
