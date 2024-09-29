from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import acceuil, signup, dashboard, addstack, allstack, chat_view, send_message, get_messages, \
    documentationfile, delete_stacks, search_view, stack_detail

urlpatterns = [
    path("", acceuil, name="acceuil"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("accounts/dashboard", dashboard, name="dashboard"),
    path("accounts/signup", signup, name="signup"),
    path('', include('django.contrib.auth.urls')),
    path('accounts/addstack/', addstack, name='addstack'),
    path('accounts/allstack/', allstack, name='allstack'),
    path('accounts/dashboard/chat/', chat_view, name='chat'),
    path('accounts/dashboard/get_messages/', get_messages, name='get_messages'),
    path('accounts/dashboard/chat/send/', send_message, name='send_message'),
    path('download/<str:filename>/', documentationfile, name='documentationfile'),
    path('accounts/delete/', delete_stacks, name='delete_stacks'),
    path('search/', search_view, name='search_view'),
    path('stack/<int:pk>/', stack_detail, name='stack_detail'),
]
