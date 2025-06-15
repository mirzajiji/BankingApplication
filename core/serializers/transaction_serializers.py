from core.models import Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()
    direction = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class  Meta:
        model = Transaction
        fields = ('id', 'sender', 'receiver', 'amount', 'created_at','direction')

    def get_sender(self, obj):
        if obj.type == 'admin_credit':
            return "Top up(Admin)"
        return obj.user.email

    def get_receiver(self, obj):
        if obj.type == 'admin_credit':
            return obj.user.email
        return obj.receiver.email if obj.receiver else None

    def get_direction(self, obj):
        request_user = self.context['request'].user

        if obj.type == 'admin_credit':
            return 'income'

        if obj.user == request_user:
            return 'outcome'
        elif obj.receiver == request_user:
            return 'income'
        return 'unknown'

    def get_created_at(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')