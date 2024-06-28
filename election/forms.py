from django import forms
from .models import Election, Candidate


class VoteForm(forms.Form):
    candidate_id = forms.ModelChoiceField(queryset=Candidate.objects.none(), widget=forms.RadioSelect)

    def __init__(self, *args, election=None, **kwargs):
        super().__init__(*args, **kwargs)
        if election:
            self.fields['candidate_id'].queryset = Candidate.objects.filter(election=election)


class EndElectionForm(forms.Form):
    election_id = forms.IntegerField(widget=forms.HiddenInput())
