# Generated by Django 2.2.28 on 2024-03-20 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LibroLink', '0006_userprofile_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='userID',
        ),
    ]