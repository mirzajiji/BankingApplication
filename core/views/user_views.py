from django.db.models.query_utils import Q

from core.models import User, BankAccount, Transaction
from core.serializers.transaction_serializers import TransactionSerializer
from core.serializers.transfer_serializers import TransferSerializer
from core.serializers.user_serializers import RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.db import models

@swagger_auto_schema(
    method='post',
    request_body=RegistrationSerializer,
    responses={201: 'User created successfully'},
    operation_description="Register a new user",
)
@api_view(['POST'])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"User registered successfully"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=TransferSerializer,
    responses={201: 'Transaction created successfully'},
    operation_description="Transfer an existing user",

)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_to_user_transaction(request):
    serializer = TransferSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        result = serializer.save()
        return Response(result, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={201: 'Get balance successfully'},
    operation_description="Get Balance",

)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account_balance(request):
    user = request.user
    try:
        balance = user.account.balance
    except:
        return Response({"error":"Account does not exist"},status=status.HTTP_404_NOT_FOUND)
    return Response({'email': user.email, 'balance': balance}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    responses={201: 'Get transactions successfully'},
    operation_description="Get transactions",

)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(
        models.Q(user=request.user) | models.Q(receiver=request.user)
    ).order_by('-created_at')


    serializer = TransactionSerializer(transactions, many=True,context={'request': request})
    return Response(serializer.data)