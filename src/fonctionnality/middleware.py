# middleware.py

from django.utils import timezone
from django.conf import settings

# class ActiveUserMiddleware:
#     active_users = set()
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if request.user.is_authenticated:
#             self.active_users.add(request.user.id)
#         response = self.get_response(request)
#         return response
#
#     @classmethod
#     def get_active_user_count(cls):
#         return len(cls.active_users)


# middleware.py
from django.utils import timezone

class OnlineUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.session['last_activity'] = timezone.now().isoformat()  # Assurez-vous que cela est bien défini
        response = self.get_response(request)
        print("Last activity:", request.session.get('last_activity'))
        return response