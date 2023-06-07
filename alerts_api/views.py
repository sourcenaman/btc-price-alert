from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from .models import *
from .pagination import StandardPagination
from django_redis import get_redis_connection
import json
# Create your views here.

cache_user = get_redis_connection('default')
cache_alert = get_redis_connection('alert')

@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def fetch_all(request):
    user_id = request.user.id

    key = json.dumps(request.GET.dict()) if request.GET.dict() else "no-filter"
    if (cache_user.hmget(user_id, key)[0]):
        return Response(json.loads(cache_user.hmget(user_id, key)[0]))
    
    if (request.GET.get("status")):
        status = list(map(lambda x: x.upper(), request.GET.get("status").split(",")))
        alerts = get_list_or_404(Alert, user__id=user_id, status__in=status)
    else:
        alerts = get_list_or_404(Alert, user__id=user_id)

    paginator = StandardPagination()
    result_page = paginator.paginate_queryset(alerts, request)
    serializer = AlertSerializer(result_page, many=True)
    paginated_resp = paginator.get_paginated_response(serializer.data)

    mapping = {
        key: json.dumps(paginated_resp.data)
    }
    cache_user.hmset(user_id, mapping)

    return paginated_resp

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_alert(request):
    user_id = request.user.id

    user = get_object_or_404(User, id=user_id)
    request.data["user"] = user.id

    serializer = AlertSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    coin = request.data["coin"]
    alert_price = request.data["alert_price"]
    user_email = request.user.email
    key = coin+":"+str(float(alert_price))
    cache_alert.sadd(key, user_email)
    cache_user.delete((user_id))

    return Response(serializer.data, status=201)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def delete_alert(request, pk):
    user_id = request.user.id
    alert = get_object_or_404(Alert, id=pk, user__id=user_id)
    data = {
        "status": "DELETED"
    }

    serializer = AlertSerializer(instance=alert, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    coin = alert.coin
    alert_price = alert.alert_price
    user_email = request.user.email
    key = coin+":"+str(alert_price)
    cache_alert.srem(key, user_email)
    cache_user.delete(user_id)

    return Response(serializer.data, status=202)

