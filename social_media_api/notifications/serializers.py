from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.ReadOnlyField(source='actor.username')
    recipient_username = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_username',
            'actor', 'actor_username',
            'verb', 'is_read', 'timestamp'
        ]
        read_only_fields = ['recipient', 'actor', 'verb', 'timestamp']