import logging
from smtplib import SMTPException

from django.core.mail import send_mail

from django.conf import settings


class SendCommunication:

    @classmethod
    def send_email(cls, subject, message, recipient_list):
        logger = logging.getLogger('django.server')
        try:
            mail_result = send_mail(
                from_email=settings.DEFAULT_FROM_EMAIL,
                subject=subject,
                message=message,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info('----SENDING MAIL-----')
            logger.info(mail_result)
        except SMTPException as e:
            logger.error(e)
