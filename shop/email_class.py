from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django_shop.settings import EMAIL_HOST_USER

class Email:

    ### Sending contact message from client to shop ###
    @staticmethod
    def send_contact_email(email, subject, message):
        html_content = render_to_string('email/message_to_shop.html', {
            'email': email,
            'subject': subject,
            'message': message,
        })

        text_content = f"""
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """

        msg = EmailMultiAlternatives(
            subject=f"New message: {subject}",
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[EMAIL_HOST_USER],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    ### Sending order summary message to shop ###
    @staticmethod
    def send_order_summary_email_to_shop(cart, total, order):
        html_content = render_to_string('email/order_message_to_admin.html', {
            'cart': cart,
            'total': total,
            'order': order
        })

        text_content = f"""
        New order received #{order.id}

        Total: {total} zł

        Customer:
        {order.first_name} {order.last_name}
        Address: {order.address_1} {f"/ {order.address_2}" if order.address_2 else ""}
        Zip: {order.zip_code}, City: {order.city}
        Phone: {order.phone}
        Email: {order.email}
        """

        subject = f"New order #{order.id}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [EMAIL_HOST_USER]
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    ### Sending order summary message to client ###
    @staticmethod
    def send_order_summary_email_to_client(cart, total, order):
        html_content = render_to_string('email/order_message_to_client.html', {
            'cart': cart,
            'total': total,
            'order': order
        })

        text_content = f"""
        Order summary #{order.id}

        Total: {total} zł

        Your informations:
        {order.first_name} {order.last_name}
        Address: {order.address_1} {f"/ {order.address_2}" if order.address_2 else ""}
        Zip: {order.zip_code}, City: {order.city}
        Phone: {order.phone}
        Email: {order.email}
        """

        subject = f"Order summary #{order.id}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [order.email]
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        msg.send()