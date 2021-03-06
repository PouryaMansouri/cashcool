# Generated by Django 3.0.7 on 2020-07-09 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('debts', '0003_auto_20200709_1807'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebtPenalty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('penalty_amount', models.DecimalField(decimal_places=0, max_digits=9)),
                ('status', models.IntegerField(choices=[(0, 'Not Payed'), (1, 'Payed')], default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('debt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='debts.Debt')),
            ],
            options={
                'db_table': 'debt_penalty',
            },
        ),
    ]
