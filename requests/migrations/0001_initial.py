# Generated by Django 3.0.7 on 2020-07-08 17:16

import credit_card.requests.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cwallets', '0001_initial'),
        ('credit_marketers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportUserRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(max_length=200, upload_to=credit_card.requests.models.ImportUserRequest.excel_file_upload_path)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Processed'), (2, 'Accepted'), (3, 'PartialAccepted'), (4, 'Rejected')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='cwallets.CWalletRegular')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketer', to='credit_marketers.CreditMarketer')),
            ],
            options={
                'db_table': 'import_user_requests',
            },
        ),
    ]
