from vapor_manager.users.models import Account


class UserAccountMiddleware(object):
    """makes user's Account publicly available to classes"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Process the request, adding account for authenticated users"""
        account = None
        if request.user.is_authenticated:
            # only authenticated users can be in accounts
            account = request.user.current_account
            if not account:
                if request.user.accounts.count() > 0:
                    account = request.user.accounts.first()
                else:
                    account = Account.objects.create(owner=request.user, company=request.user.email)
                    account.users.add(request.user)
                request.user.current_account = account
                request.user.save()
        request.account = account

        response = self.get_response(request)

        return response
