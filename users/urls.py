from django.urls import path
from . import views as user_view

urlpatterns = [
    path('dashboard/', user_view.dashboard, name='dashboard'),
    path('offline/', user_view.offline, name='offline'),
    path('delete-account/', user_view.delete_account, name='delete_account'),

]