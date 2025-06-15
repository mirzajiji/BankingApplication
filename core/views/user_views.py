
from core.models import User, BankAccount, Transaction
from core.serializers.transaction_serializers import TransactionSerializer
from core.serializers.transfer_serializers import TransferSerializer
from core.serializers.user_serializers import RegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
    manual_parameters=[
        openapi.Parameter('direction', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        openapi.Parameter('min_amount', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_amount', openapi.IN_QUERY, type=openapi.TYPE_NUMBER),
        openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
        openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
    ],
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
    direction = request.query_params.get('direction')
    min_amount = request.query_params.get('min_amount')
    max_amount = request.query_params.get('max_amount')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    if direction:
        if direction == 'income':
            transactions = transactions.filter(receiver=user)
        elif direction == 'outcome':
            transactions = transactions.filter(user=user)
    if min_amount:
        transactions = transactions.filter(amount__gte=min_amount)
    if max_amount:
        transactions = transactions.filter(amount__lte=max_amount)
    if start_date:
        transactions = transactions.filter(created_at__date__gte=start_date)
    if end_date:
        transactions = transactions.filter(created_at__date__lte=end_date)

    transactions = transactions.order_by('-created_at')
    serializer = TransactionSerializer(transactions, many=True, context={'request': request})
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'id',
            openapi.IN_QUERY,
            description="Transaction ID",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={200: "Get transaction successfully"},
    operation_description="Get a specific transaction by ID",
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_transaction_by_id(request):
    transaction_id = request.query_params.get('id')

    if not transaction_id:
        return Response({"error": "Transaction ID is required"}, status=400)

    try:
        transaction = Transaction.objects.get(id=transaction_id)
    except Transaction.DoesNotExist:
        return Response({"error": "Transaction not found"}, status=404)

    serializer = TransactionSerializer(transaction, context={'request': request})
    return Response(serializer.data, status=200)