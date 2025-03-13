from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from loguru import logger

def send_otp_email(email: str, otp: str):
    subject = _("Your OTP for Login")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    context = {
        "otp": otp,
        "expiry_time": settings.OTP_EXPIRATION,
        "site_name": settings.SITE_NAME,
    }
    html_email = render_to_string("emails/opt_email.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    try:
        email.send()
        logger.info(f"OTP email sent to {email}")
    except Exception as e:
        logger.error(f"Error sending OTP email to {email}: {str(e)}")


def send_account_locked_email(self):
    subject = _("Your account has been locked")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [self.email]
    context = {
        "user": self,
        "lockout_duration": int(settings.LOCKOUT_DURATION.total_seconds() // 60),
        "site_name": settings.SITE_NAME,
    }
    html_email = render_to_string("emails/account_locked.html", context)
    plain_email = strip_tags(html_email)
    email = EmailMultiAlternatives(subject, plain_email, from_email, recipient_list)
    email.attach_alternative(html_email, "text/html")
    try:
        email.send()
        logger.info(f"Account locked email sent to {self.email}")
    except Exception as e:
        logger.error(f"Failed to send accoutn locked email to {self.email}: {str(e)}")
