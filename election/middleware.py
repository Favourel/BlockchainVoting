# from django.utils.deprecation import MiddlewareMixin
# from .models import Election
# from users.models import Notification
# import datetime
#
#
# class NotificationMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         current_time = datetime.datetime.now()
#         active_elections = Election.objects.filter(is_active=True)
#         for election in active_elections:
#             if election.start_time <= current_time <= election.end_time:
#                 Notification.objects.get_or_create(
#                     title=f"Election Started: {election.title}",
#                     message=f"The election '{election.title}' is now ongoing.",
#                     is_active=True
#                 )
#             elif current_time > election.end_time:
#                 election.is_active = False
#                 election.save()
#                 Notification.objects.get_or_create(
#                     title=f"Election Ended: {election.title}",
#                     message=f"The election '{election.title}' has ended.",
#                     is_active=True
#                 )
