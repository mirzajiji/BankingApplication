from decimal import Decimal

from core.models import User, Transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_add_balance(request):
    email = request.data.get('email')
    amount = request.data.get('amount')

    try:
        user = User.objects.get(email=email)
        account = user.account
        account.balance += Decimal(str(amount))
        account.save()

        Transaction.objects.create(
            user = user,
            amount = amount,
            type='admin_credit',
        )

        return Response({'message': f'{amount} added to {email}'}, status=200)
    except User.DoesNotExist:
        return Response({'message': 'User does not exist'}, status=404)