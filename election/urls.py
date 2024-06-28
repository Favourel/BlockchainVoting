from django.urls import path
from . import views as election_view

urlpatterns = [
    path('election/<int:election_id>/', election_view.show_election, name='show_election'),
    path('election/<int:election_id>/vote/', election_view.vote, name='vote'),
    path('election/<int:election_id>/confirmation/', election_view.vote_confirmation, name='vote_confirmation'),
    path('election/<int:election_id>/results/', election_view.live_results, name='live_results'),
    path('election/<int:election_id>/end/', election_view.end_election, name='end_election'),

]
