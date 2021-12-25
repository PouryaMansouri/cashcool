# Generated by Django 3.0.7 on 2020-07-08 17:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('credit_cwallets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=9, validators=[django.core.validators.MinValueValidator(1)])),
                ('ptc', models.CharField(max_length=256)),
                ('error_explanation', models.TextField(blank=True, null=True)),
                ('commission_transaction', models.BooleanField(default=False)),
                ('commission_transaction_parent', models.IntegerField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Success'), (2, 'Cancel'), (3, 'Reject')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='club_or_credit_cwallet', to='credit_cwallets.CreditCwallet')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_cwallet', to='credit_cwallets.CreditCwallet')),
            ],
            options={
                'db_table': 'credit_transaction',
            },
        ),
    ]