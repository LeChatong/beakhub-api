import os
from email.mine.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template import loader

from BeakHub import settings


class MailingBuilder:
    """ Class for building template mail who would be sending """

    def __init__(self, subject, content, template, email_sender, email_receiver):

        html_message = loader.render_to_string(template, content)

        msg = EmailMultiAlternatives(subject, html_message, email_sender, [email_receiver])
        msg.attach_alternative(html_message, "text/html")
        msg.mixed_subtype = 'related'

        # Add Image
        file_path_logo_png = os.path.join(settings.MEDIA_ROOT+"/mail/", "beak_solo.png")
        with open(file_path_logo_png, 'rb') as f:
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<{name}>'.format(name="beak_solo.png"))
            logo.add_header('Content-Disposition', 'inline', filename="beak_solo.png")
        msg.attach(logo)

        msg.send()
