# Generated by Django 4.2.4 on 2023-10-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0027_profile_friends'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]