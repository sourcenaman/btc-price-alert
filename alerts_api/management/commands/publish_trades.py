from django.core.management.base import BaseCommand
import websocket, rel, json
from django_redis import get_redis_connection

class Command(BaseCommand):

    trade_queue = get_redis_connection('trade')

    def on_message(self, ws, message):
        message = json.loads(message)
        try:
            self.trade_queue.lpush("BTCUSDT", float('%.2f' % float(message["p"])))
        except Exception as e:
            print(e)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")

    def handle(self, *args, **options):
        ws = websocket.WebSocketApp("wss://stream.binance.com:443/ws/btcusdt@trade",
                                on_open=self.on_open,
                                on_message=self.on_message,
                                on_error=self.on_error,
                                on_close=self.on_close)

        # Set dispatcher to automatic reconnection, 5 second reconnect delay when connection closed by binance.
        ws.run_forever(dispatcher=rel, reconnect=5)
        rel.signal(2, rel.abort)
        rel.dispatch()
