from django.conf import settings


def settings_context(_request):
    return {"settings": settings}


def user_context(request):
    return {'user': request.user}


def account_context(request):
    if request.user.is_authenticated:
        return {'account': request.user.current_account}
    return {'account': None}
