from django.core.management.base import BaseCommand
from django_redis import get_redis_connection
import time
from alerts_api.tasks import send_email

class Command(BaseCommand):

    trade_queue = get_redis_connection('trade')
    cache_alert = get_redis_connection('alert')

    def handle(self, *args, **options):
        last_highest = 0
        last_lowest = 0
        while True:
            try:
                curr_len = self.trade_queue.llen('BTCUSDT')
                trades = self.trade_queue.rpop('BTCUSDT', curr_len)

                if curr_len:
                    highest = float(max(trades))
                    lowest = float(min(trades))
                    if last_highest != highest and last_lowest != lowest:
                        last_highest = highest
                        last_lowest = lowest
                        print(highest, lowest)
                        for i in range(round(lowest*100), round(highest*100)+1):
                            price = round(i/100, 4)
                            key = "BTCUSDT"+":"+str(price)
                            alert_emails = self.cache_alert.smembers(key)
                            for email in alert_emails:
                                send_email.delay(email.decode('ASCII'), price, "BTCUSDT")
                time.sleep(5)
            except Exception as e:
                print(e)
                time.sleep(5)
