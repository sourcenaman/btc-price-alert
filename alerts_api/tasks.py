from celery import shared_task
from .models import Alert

@shared_task
def send_email(email, price, coin):
    print(f'Email sent to {email} for USD{price}')
    alert = Alert.objects.get(user__email=email, alert_price=price, coin=coin)
    alert.status = "TRIGGERED"
    alert.save()
    print(f'Entry updated for {email}')

