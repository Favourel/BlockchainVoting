from datetime import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, redirect

from election.models import Election, Vote
from users.models import Notification


# Create your views here.


@login_required
def dashboard(request):
    elections = Election.objects.filter(is_active=True, start_time__lte=datetime.now(),
                                        end_time__gte=datetime.now())
    notifications = Notification.objects.filter(is_active=True)

    if Vote.objects.filter(user=request.user).exists():
        my_votes = Vote.objects.filter(user=request.user)
    else:
        my_votes = ""
    context = {
        'elections': elections,
        'notifications': notifications,
        'my_votes': my_votes,
        "now": datetime.now().hour,
    }

    return render(request, 'users/dashboard.html', context)


def offline(request):
    return render(request, 'users/offline.html', {})


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('login')