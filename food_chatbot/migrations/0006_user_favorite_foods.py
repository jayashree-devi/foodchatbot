# Generated by Django 5.1.4 on 2025-01-05 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_chatbot', '0005_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite_foods',
            field=models.JSONField(null=True),
        ),
    ]
