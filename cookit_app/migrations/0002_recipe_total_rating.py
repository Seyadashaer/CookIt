# Generated by Django 4.1.5 on 2023-01-31 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookit_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='total_rating',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
