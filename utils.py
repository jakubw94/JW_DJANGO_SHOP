from django import forms
from django.template.loader import render_to_string
from django.contrib import messages


# Adding "form-control" to form fields #
class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_classes = field.widget.attrs.get('class', '')
            classes = (existing_classes + ' form-control').strip()
            field.widget.attrs['class'] = classes


### Email placeholder for app demo version - renders email as message (messages) ###
def preview_email_message(request, email, subject, message_text, setting):

    if setting == "message_to_shop":
        context = {
            "email": email,
            "subject": subject,
            "message": message_text,
        }
        template = "message_to_shop.html"
    elif setting == "order":
        context = {
            'cart': email,
            'total': subject,
            'order': message_text
        }
        template = "order_review.html"

    email_html = render_to_string(f"email/{template}", context)

    messages.add_message(
        request,
        messages.INFO,
        email_html,
        extra_tags="email-preview"
    )