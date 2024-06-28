from django.contrib import admin
from .models import Election, Candidate, Vote, Block


class ElectionAdmin(admin.ModelAdmin):
    list_display = ["title", "start_time", "end_time"]


class CandidateAdmin(admin.ModelAdmin):
    list_display = ["name", "election"]


class VoteAdmin(admin.ModelAdmin):
    list_display = ["user", "candidate", "timestamp"]


admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Block)

