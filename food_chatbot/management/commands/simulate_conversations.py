import random, os, django
from django.core.management.base import BaseCommand
from food_chatbot.models import User, Conversation
from openai import OpenAI
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eitr_chatbot.settings")
django.setup()

class Command(BaseCommand):
    help = 'Simulate 100 user conversations and store their favorite foods and dietary preferences'

    def handle(self, *args, **kwargs):
        FOOD_CHOICES = ["Burrito", "Pizza", "Burger", "Pasta", "Sushi", "Tacos", "Chicken Salad", "Ice Cream",
                        "Steak", "Fried Chicken", "Biriyani", "Rice", "Veggie salad", "Fruit Juice"]
        vegetarian_foods = ["Veggie salad", "Pasta", "Sushi", "Tacos", "Rice", "Ice Cream", "Fruit Juice"]

        for i in range(1, 101):
            # Randomly assign whether the user is vegetarian
            is_vegetarian = random.choice([True, False])

            # Select top 3 favorite foods
            if is_vegetarian:
                favorite_foods = random.sample(vegetarian_foods, 3)
            else:
                favorite_foods = random.sample(FOOD_CHOICES, 3)

            # Create the user in the database
            user, created = User.objects.get_or_create(
                name=f"User{i}"
            )
            user_message = ', '.join(favorite_foods)
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
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created and Simulated User{i}"))
            else:
                # self.stdout.write(self.style.SUCCESS(f"Simulated User{i}"))
                break
