# Generated by Django 5.1.4 on 2025-01-05 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_chatbot', '0003_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]