from rest_framework import serializers
from .models import Alert, User
from django.db.models import Q

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class AlertSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=False)
    coin = serializers.CharField(required=True, max_length=10)
    alert_price = serializers.FloatField(required=True)
    status = serializers.CharField(default="CREATED")

    def create(self, validated_data):
        if "status" in validated_data.keys():
            del validated_data["status"]
        limit = 50
        alerts_count = Alert.objects.filter(
            user__id=validated_data["user"].id, 
            coin=validated_data["coin"],
            status__in=["CREATED", "TRIGGERED"]
            ).count()
        same_alert = Alert.objects.filter(
            user__id=validated_data["user"].id, 
            coin=validated_data["coin"],
            alert_price=validated_data["alert_price"]
        )
        if alerts_count >= limit:
            raise serializers.ValidationError(f"Only {limit} active alerts allowed per coin.")
        if same_alert.count():
            if same_alert and same_alert[0].status == "DELETED":
                return self.update(same_alert[0], {
                    "status": "CREATED"
                })
            else:
                raise serializers.ValidationError(f"Alert for {validated_data['coin']} at price {validated_data['alert_price']} already exists.")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if validated_data["status"] == "CREATED":
            pass
        elif instance.status == "DELETED":
            raise serializers.ValidationError(f"Alert already deleted.")
        return super().update(instance, validated_data)


    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        del representation['user']
        return representation

    class Meta:
        model = Alert
        exclude = ["created_at", "updated_at"]




