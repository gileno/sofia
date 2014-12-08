from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template import loader
from django.utils.html import strip_tags


def send_mail_template(
    subject, template_name, context, recipient_list,
    from_email=settings.DEFAULT_FROM_EMAIL, commit=True
):
    context.update(settings.CONTEXT_EXTRA_MAIL)
    html_content = loader.render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, recipient_list
    )
    msg.attach_alternative(html_content, "text/html")
    if commit:
        msg.send()
    return msg
