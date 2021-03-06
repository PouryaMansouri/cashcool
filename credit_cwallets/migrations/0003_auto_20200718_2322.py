# Generated by Django 3.0.7 on 2020-07-18 18:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit_cwallets', '0002_creditcwallet_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcwallet',
            name='balance',
            field=models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MaxValueValidator(1000000000), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='creditcwallet',
            name='credit_amount',
            field=models.DecimalField(decimal_places=0, max_digits=10, validators=[django.core.validators.MaxValueValidator(1000000000), django.core.validators.MinValueValidator(0)]),
        ),
    ]
