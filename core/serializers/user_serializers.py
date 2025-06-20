from rest_framework import serializers
from core.models import User, BankAccount


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        BankAccount.objects.create(user=user)
        return user
