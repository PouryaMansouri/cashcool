# Generated by Django 3.0.7 on 2020-07-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_cwallets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcwallet',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]