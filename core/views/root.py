from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        "login": reverse('token_obtain_pair', request=request),
        "register": reverse('register', request=request),
        "refresh": reverse('token_refresh', request=request),
        "fill_balance": reverse('admin_add_balance', request=request),
        "transfer": reverse('user_to_user_transaction',request=request),
        "balance": reverse('get_account_balance', request=request),

    })
