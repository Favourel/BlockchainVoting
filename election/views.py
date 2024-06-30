from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_exempt

from .forms import VoteForm, EndElectionForm
from .models import Election, Candidate, Vote
from users.models import Notification
from .blockchain import Blockchain
import requests
import datetime
from datetime import datetime

from django.core.mail import send_mail


blockchain = Blockchain()


# Create your views here.


@login_required
def show_election(request, election_id):
    election = Election.objects.get(id=election_id)
    candidates = Candidate.objects.filter(election=election)
    if request.method == 'POST':
        form = VoteForm(request.POST, election=election)
        if form.is_valid():
            candidate_id = form.cleaned_data['candidate_id']
            candidate = Candidate.objects.get(id=candidate_id)
            vote = Vote(student=request.user, candidate=candidate)
            vote.save()
            blockchain.add_vote(vote)
            return redirect('vote_confirmation', election_id=election_id)
    else:
        form = VoteForm(election=election)
    return render(request, 'election/elections.html', {'election': election, 'form': form, "candidates": candidates, "now": datetime.now().hour,})


@login_required
@csrf_exempt
def vote(request, election_id):
    election = Election.objects.get(id=election_id)
    student = request.user._wrapped if isinstance(request.user, SimpleLazyObject) else request.user

    try:
        # Check if the user has already voted in this election
        Vote.objects.get(user=student, candidate__election=election)
        # If vote exists, render the already voted template
        return render(request, 'election/already_voted.html', {'election': election})
    except ObjectDoesNotExist:
        # If no vote exists, proceed to voting
        if request.method == 'POST':
            form = VoteForm(request.POST, election=election)
            if form.is_valid():
                candidate = form.cleaned_data['candidate']
                vote = Vote.objects.create(user=student, candidate=candidate)
                blockchain.add_vote(vote)
                return redirect('vote_confirmation', election_id=election.id)
        else:
            form = VoteForm(election=election)
        return render(request, 'election/elections.html', {'election': election, 'form': form, "now": datetime.now().hour,})


@login_required
def vote_confirmation(request, election_id):
    election = Election.objects.get(id=election_id)
    context = {
        'election': election,
        "now": datetime.now().hour,
    }
    return render(request, 'election/vote_confirmation.html', context)


@login_required
def live_results(request, election_id):
    election = Election.objects.get(id=election_id)
    candidates = Candidate.objects.filter(election=election)
    vote_counts = blockchain.get_vote_counts()
    results = {candidate.name: vote_counts.get(candidate.name, 0) for candidate in candidates}
    context = {
        'election': election,
        'results': results
    }
    return render(request, 'election/live_results.html', context)


@login_required
def end_election(request, election_id):
    election = Election.objects.get(id=election_id)
    if request.method == 'POST':
        form = EndElectionForm(request.POST)
        if form.is_valid():
            election.is_active = False
            election.save()
            if blockchain.is_chain_valid():
                Notification.objects.create(
                    title="Election Ended",
                    message=f"The election '{election.title}' has ended and results are now final.",
                    is_active=True
                )
            return redirect('dashboard')
    else:
        form = EndElectionForm(initial={'election_id': election.id})
    return render(request, 'election/end_election.html', {'election': election, 'form': form})


def send_email_notification(student_email, subject, message):
    send_mail(
        subject,
        message,
        'admin@school.com',
        [student_email],
        fail_silently=False,
    )