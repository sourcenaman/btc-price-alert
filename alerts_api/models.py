from django.db.models import *
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

#inheriting django's built-in auth model
class User(AbstractUser):
    name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Alert(BaseModel):
    STATUS = (
        ('CREATED', 'created'),
        ('TRIGGERED', 'triggered'),
        ('DELETED', 'deleted')
    )
    user = ForeignKey(User, related_name='alerts', on_delete=CASCADE)
    coin = CharField(max_length=10)
    '''
    Decimal is not used because
    1. max_digits and decimal_places were required
    2. Even though float suffers from rounding issues, we are not going to do any arithematic operations on it.
    '''
    alert_price = FloatField()
    status = CharField(choices=STATUS, default="CREATED")

    class Meta:
        indexes = [
            #useful for getting data for sending alerts
            Index(fields=['coin', 'alert_price', 'status']),
            #useful for status filter
            Index(fields=['status'])
        ]
        ordering = ("-updated_at", "coin")

    def __str__(self):
        return f"Price alert of {self.alert_price} on {self.coin}"

    


