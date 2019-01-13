from threading import Thread

from rentalmoose.classes.MailchimpHandler import *

#     list_id = "ec09a29d85"


#
# MailchimpHandler.get_tag_id('Tenant', 'ec09a29d85')
MailchimpHandler.add_subscriber("aninhasilva@gmail.com", "ainha", "Silva")
MailchimpHandler.attach_tags(['Tenant'], "aninhasilva@gmail.com")




