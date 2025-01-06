from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
from openai import OpenAI
import json
from django.conf import settings
import os
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import User, Conversation
import random

FOOD_CHOICES = ["Burrito", "Pizza", "Burger", "Pasta", "Sushi", "Tacos", "Chicken Salad", "Ice Cream",
                "Steak", "Fried Chicken", "Biriyani", "Rice", "Veggie salad", "Fruit Juice"]
vegetarian_foods = ["Veggie salad", "Pasta", "Sushi", "Tacos", "Rice", "Ice Cream", "Fruit Juice"]

def homeView(request):
    # Reset the session when loading the page to capture anonymous user and its food choices
    request.session.flush()
    return render(request, 'layout.html')

@csrf_exempt
def chatbot_message(request):
    print(request)
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=400)

    try:
        data = json.loads(request.body)
        # Check session key and create if it does not exist
        session_key = request.session.session_key or request.session.create() or request.session.session_key
        # Get or create the user based on session key
        user, created = User.objects.get_or_create(session_key=session_key)
        if created:
            user.name = f"guest{user.id}"
            user.save()

        user_message = data.get("message", "")
        if not user_message:
            return JsonResponse({"response": "Please provide a message."})

        # Manage favorite foods selection
        favorite_foods = request.session.get('favorite_foods', [])
        if len(favorite_foods) < 3:
            if user_message not in FOOD_CHOICES:
                if not favorite_foods:
                    initial_prompt = "Hello! Please choose your top 3 favorite foods from the following list:\n" + "\n".join(FOOD_CHOICES)
                    return JsonResponse({"response": initial_prompt})
                return JsonResponse({"response": "Please select a valid food from the list."})

            favorite_foods.append(user_message)
            request.session['favorite_foods'] = favorite_foods

            if len(favorite_foods) < 3:
                remaining_choices = 3 - len(favorite_foods)
                return JsonResponse({"response": f"Please select {remaining_choices} more food(s) from the list."})

        # If 3 foods are selected, determine vegetarian status and save
        if len(favorite_foods) == 3:
            is_user_vegetarian = all(food in vegetarian_foods for food in favorite_foods)
            user.is_vegetarian = is_user_vegetarian
            user.favorite_foods = favorite_foods
            user.save()
            if user_message is not None:
                user_message = ', '.join(favorite_foods) + '\n'+user_message
            else:
                user_message = ', '.join(favorite_foods)
            # summary_message = f"Your favorite foods are: {', '.join(favorite_foods)}."
            # diet_status = "You are vegetarian." if is_user_vegetarian else "You are not vegetarian."
            # return JsonResponse({"response": f"{summary_message} {diet_status}"})

        # Interact with OpenAI's ChatGPT
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a chatbot that helps users list their three favorite foods."},
                {"role": "user", "content": user_message}
            ],
            model="gpt-4o"
        )
        bot_message = chat_completion.choices[0].message.content
        Conversation.objects.create(user=user, user_message=user_message, bot_response=bot_message)

        return JsonResponse({"response": bot_message})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vegetarian_users(request):
    users = User.objects.filter(is_vegetarian=True)
    data = [
        {
            "name": user.name,
            "is_vegetarian": user.is_vegetarian,
            "top_foods": user.favorite_foods
        }
        for user in users
    ]
    return Response(data)
