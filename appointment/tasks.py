from celery import shared_task


@shared_task
def send_email_appointment(email):
    email.send(fail_silently=False)
    return None
