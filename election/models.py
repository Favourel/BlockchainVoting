from django.db import models
from hashlib import sha256
import datetime
import random
from django.conf import settings
from django.utils import timezone
from django.utils.functional import SimpleLazyObject


class Election(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(default='profile_picture/edit.png', upload_to='profile_picture')
    profile = models.TextField()
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)  # Replace with your logic for generating a unique transaction ID

    def __str__(self):
        return f"{self.user} voted for {self.candidate}"


class Block(models.Model):
    timestamp = models.DateTimeField()
    vote = models.OneToOneField(Vote, on_delete=models.CASCADE, null=True)
    previous_hash = models.CharField(max_length=64, null=True, blank=True)
    hash = models.CharField(max_length=64)
    nonce = models.IntegerField()

    def calculate_hash(self):
        # Ensure all components are converted to strings properly
        timestamp_str = str(self.timestamp)

        # Extract relevant user information
        if isinstance(self.vote.user, SimpleLazyObject):
            user_obj = self.vote.user._wrapped
        else:
            user_obj = self.vote.user

        user_str = user_obj if user_obj else ""  # Convert user object to string using matric number
        candidate_name_str = self.vote.candidate.name if self.vote and self.vote.candidate else ""
        previous_hash_str = self.previous_hash if self.previous_hash else ""
        nonce_str = str(self.nonce)

        # Concatenate all parts into the checksum
        checksum = timestamp_str + str(user_str) + candidate_name_str + previous_hash_str + nonce_str
        return sha256(checksum.encode("utf-8")).hexdigest()


