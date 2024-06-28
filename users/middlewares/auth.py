from django.shortcuts import redirect
from django.contrib import messages


def LogoutCheckMiddleware(get_response):
    def middleware(request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return get_response(request)
    return middleware
