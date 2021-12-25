# Generated by Django 3.0.7 on 2020-07-08 17:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cwallets', '0001_initial'),
        ('demands_settings', '0001_initial'),
        ('credit_marketers', '0001_initial'),
        ('account_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCwallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('personal', 'personal'), ('business', 'business')], default='personal', max_length=20)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='user_data/qr_code/')),
                ('credit_amount', models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[django.core.validators.MaxValueValidator(1000000000), django.core.validators.MinValueValidator(0)])),
                ('balance', models.DecimalField(decimal_places=0, default=0, max_digits=10, validators=[django.core.validators.MaxValueValidator(1000000000), django.core.validators.MinValueValidator(0)])),
                ('checkout_period_month', models.PositiveIntegerField()),
                ('status', models.IntegerField(choices=[(0, 'inactive'), (1, 'active'), (2, 'banned')], default=1)),
                ('is_demand', models.BooleanField(default=False)),
                ('cc_custom_setting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_settings.AccountSettings')),
                ('credit_marketer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='credit_marketers.CreditMarketer')),
                ('current_cashtag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cwallets.Cashtags')),
                ('cwallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cwallets.CWalletRegular')),
                ('demand_setting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='demands_settings.DemandSetting')),
            ],
            options={
                'db_table': 'credit_cwallet',
            },
        ),
    ]