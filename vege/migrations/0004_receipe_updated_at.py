# Generated by Django 5.1.4 on 2025-01-14 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vege', '0003_receipe_receipe_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipe',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
