from celery import shared_task
from .models import Alert
from django_redis import get_redis_connection

@shared_task
def send_email(email, price, coin):
    cache_user = get_redis_connection('default')
    print(f'Email sent to {email} for USD{price}')
    alert = Alert.objects.get(user__email=email, alert_price=price, coin=coin)
    user_id = alert.user.id
    alert.status = "TRIGGERED"
    alert.save()
    cache_user.delete(user_id)
    print(f'Entry updated for {email}')

