from coreapi import Object
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from helper.constant import CURRENT_SITE_URL

from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class DBoardUtil(Object):

    def sent_email(self, request, profile, mail_subject, render_string='acc_active_email.html'):

        message = render_to_string(render_string, {
            'user': profile,
            'domain': CURRENT_SITE_URL,
            'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
            'token': account_activation_token.make_token(profile),
        })

        # to_email = form.cleaned_data.get('email')

        email = EmailMessage(
            mail_subject, message, to=[profile.email]
        )
        email.send()
        messages.success(request,
                         "An activation url is sent to your email. Please verify. Don't forget to check spam if not in inbox.")


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_email_verified)
        )


account_activation_token = TokenGenerator()
