from django.core.mail import EmailMessage

from celery import shared_task


@shared_task
def send_email(data):
    EmailMessage.send(
            subject=data['email_subject'], 
            body=data['email_body'], 
            to=[data['to_email']],
            fail_silently=False)
    # return email.send(fail_silently=False)
    return None
