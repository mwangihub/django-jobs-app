import json
from asgiref.sync import async_to_sync as _sync
from channels.db import database_sync_to_async as db_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from channels.consumer import AsyncConsumer, SyncConsumer
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User  # , ConnectionHistory, AboutWeb
from .views import ConnectionHistorySerializer
import channels.layers
from django.contrib.auth.signals import (user_logged_in, user_logged_out)
from django.contrib import messages
User = get_user_model()


def _user_logs():
    online = list()
    offline = list()
    qs = User.objects.filter(log__logged=True).exclude(
        Q(admin=False) & Q(staff=False) & Q(active=False)).values()
    qs2 = User.objects.filter(log__logged=False).exclude(
        Q(admin=False) & Q(staff=False) & Q(active=False)).values()
    for i in qs2:
        obj = i.copy()
        del obj['last_login']
        offline.append(obj)
    for i in qs:
        obj = i.copy()
        del obj['last_login']
        online.append(obj)
    data = {
        'online': online,
        'offline': offline,
    }
    return data


class DashConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print('connect', event)
        self.room_name = 'dashboard_chart_data'
        _sync(self.channel_layer.group_add)(
            self.room_name,
            self.channel_name
        )

        self.send({
            "type": "websocket.accept"
        })

    def websocket_receive(self, event):
        print('received', event['text'])
        data = {
            'id': json.loads(event['text']).get('id'),
            'delete_temp': json.loads(event['text']).get('delete_temp'),
        }
        print(data)

        # try:
        #     instance = AboutWeb.objects.get(id=data.get('id'))
        #     instance.delete()
        #     data['msg'] = "Template removed"
        #     self.send({
        #         "type": "websocket.send", "text": json.dumps(data)
        #     })
        # except AboutWeb.DoesNotExist:
        #     data['msg'] = "That template don't exist."
        #     data['delete_temp'] = False

        #     self.send({
        #         "type": "websocket.send", "text": json.dumps(data)
        #     })

    def websocket_message(self, event):
        self.send({
            "type": "websocket.send", "text": json.dumps(event)
        })

    def websocket_disconnect(self, event):
        print('disconnect', event)

    @staticmethod
    @receiver(user_logged_in)
    def log_user_login(sender, request, user, **kwargs):
        print('trigger login consumer*')

        # instance = ConnectionHistory.objects.filter(user=user)
        # if not instance:
        #     ConnectionHistory.objects.get_or_create(user=user, logged=True)
        # else:
        #     ConnectionHistory.objects.filter(user=user).update(logged=True)
        # qs = ConnectionHistory.objects.all()
        # data = ConnectionHistorySerializer(qs, many=True)
        # layer = channels.layers.get_channel_layer()
        # _sync(layer.group_send)('dashboard_chart_data', {
        #     'type': 'websocket.message',
        #     'data': data.data,
        #     'users': True
        # })

    @staticmethod
    @receiver(user_logged_out)
    def log_user_logout(sender, request, user, **kwargs):
        print('trigger logout consumer*')
        # ConnectionHistory.objects.filter(user=user).update(logged=False)
        # qs = ConnectionHistory.objects.all()
        # data = ConnectionHistorySerializer(qs, many=True)
        # layer = channels.layers.get_channel_layer()
        # _sync(layer.group_send)('dashboard_chart_data', {
        #     'type': 'websocket.message',
        #     'data': data.data,
        #     'users': True
        # })

    @staticmethod
    @receiver(post_save, sender=User)
    def user_chart_receiver(sender,  update_fields, **kwargs):
        print('*************** trigger chart consumer ******************')
        # data = {
        #     'admin': User.objects.all().filter(admin=True).count(),
        #     'staff': User.objects.all().filter(Q(admin=False) & Q(staff=True)).count(),
        #     'active': User.objects.all().filter(Q(admin=False) & Q(staff=False) & Q(active=True)).count(),
        #     'inactive': User.objects.all().filter(Q(admin=False) & Q(staff=False) & Q(active=False)).count(),
        # }
        # layer = channels.layers.get_channel_layer()
        # _sync(layer.group_send)('dashboard_chart_data', {
        #     'type': 'websocket.message',
        #     'data': data,
        #     'chart': True
        # })
