from decimal import Decimal

from rest_framework import serializers
from core.models import User, Transaction


class TransferSerializer(serializers.Serializer):
    receiver_email = serializers.EmailField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate(self, data):
        sender = self.context["request"].user
        receiver_email = data["receiver_email"]
        amount = data["amount"]

        if not isinstance(amount, Decimal):
            raise serializers.ValidationError("Amount must be a valid number.")

        if sender.email == receiver_email:
            raise serializers.ValidationError("You cannot transfer money to yourself.")
        try:
            receiver = User.objects.get(email=receiver_email)
        except:
            raise serializers.ValidationError("Receiver doesn't exist.")

        if sender.account.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")
        data["receiver"] = receiver
        return data

    def create(self, validated_data):
        sender = self.context["request"].user
        receiver = validated_data["receiver"]
        amount = validated_data["amount"]

        sender.account.balance -= amount
        sender.account.save()

        receiver.account.balance += amount
        receiver.account.save()

        Transaction.objects.create(
            user=sender,
            receiver=receiver,
            amount=amount,
            type="user_transfer",
        )

        return {
            "message": f"{amount} transferred to {receiver.email}",
            "balance": sender.account.balance,
        }
