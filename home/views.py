from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.utils.html import format_html


def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')


@require_POST
def contact(request):
    """ A view to send an email to the store """

    if request.method == 'POST':
        name = request.POST.get('name')
        cust_email = request.POST.get('email')
        store_email = settings.DEFAULT_FROM_EMAIL
        message = request.POST.get('message')
        enquiry_body = render_to_string(
            'home/contact_emails/contact_email_body.txt',
            {'name': name, 'email': cust_email, 'message': message})
        confirmation_body = render_to_string(
            'home/contact_emails/contact_confirmation_email_body.txt',
            {'name': name, 'email': cust_email, 'message': message,
             'store_email': store_email})

        try:
            # Send customer message to store owner
            send_mail(
                'New Customer Enquiry',
                enquiry_body,
                store_email,
                [store_email],
            )

            # Send confirmation email to customer
            send_mail(
                'Thank you for your enquiry',
                confirmation_body,
                store_email,
                [cust_email],
            )
            messages.success(
                request, 'Your message has been sent! We will get back to you \
                    as soon as possible.'
                )
        except Exception as e:  # NOQA
            print(e)
            error_message = f'Sorry, your message could not be sent. Please \
                    try again later. If this issue persists, please email us \
                    at <br><a href="mailto:{store_email}">{store_email}</a>'
            messages.error(request, format_html(error_message))

    return redirect('home')
