from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name="home"),
    path("food_chatbot/chat", views.chatbot_message, name="chatbot_message"),
    path("food_chatbot/get_veg_users", views.get_vegetarian_users, name="get_vegetarian_users"),
]