from threading import Thread

from django.core.mail import send_mail
from django.template.loader import render_to_string

from hackachieve.settings import TEMPLATES_PATH
from hackachieve.classes.Environment import *
from hackachieve.settings import HOST_NAME, API_HOST, ENV


class EmailHandler(Thread):

    @staticmethod
    def trigger_email(subject, to, filename, params, from_email="Hackachieve <admin@hackachieve.com>", ):
        # both txt and html should be named the same, and they should be inside a folder with the same name!
        # eg. /templates/emails/welcome/welcome.txt
        # /templates/emails/welcome/welcome.html

        plain_text_path = TEMPLATES_PATH + "/templates/emails/{}/".format(filename) + filename + ".txt"
        html_path = TEMPLATES_PATH + "/templates/emails/{}/".format(filename) + filename + ".html"

        params['support_email'] = Environment.getkey('support_email')
        params['host_name'] = HOST_NAME
        params['api_host'] = HOST_NAME

        msg_plain = render_to_string(plain_text_path, params)
        msg_html = render_to_string(html_path, params)

        print("email sent")

        return send_mail(
            subject,
            msg_plain,
            from_email,
            to,
            html_message=msg_html,
        )

    @staticmethod
    def send_email(subject, to, filename, params, from_email="hackachieve <admin@hackachieve.ca>", ):

        TURNED_OFF_ON_DEV = Environment.getkey('turn_off_transactional_emails_on_dev')
        print("skipping email sending. If you want to turn on this feature on dev, check EmailHandler.py")

        if ENV is "dev":
            if TURNED_OFF_ON_DEV is True:  # avoid sending emails on dev mode
                return None

        print("threading and sending e-mail to {} - subject: {}".format(to, subject))

        t1 = Thread(target=EmailHandler.trigger_email, args=(subject, to, filename, params, from_email))
        t1.start()

        return t1
