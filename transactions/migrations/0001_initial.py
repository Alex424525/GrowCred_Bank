# Generated by Django 5.1.7 on 2025-04-03 18:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepositModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_at', models.DateTimeField(auto_now_add=True, verbose_name='입금 시간')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='입금')),
                ('description', models.TextField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to='accounts.account')),
            ],
            options={
                'ordering': ['-deposit_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WithdrawalModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawal_at', models.DateTimeField(auto_now_add=True, verbose_name='출금 시간')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='출금')),
                ('description', models.TextField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='withdrawals', to='accounts.account')),
            ],
            options={
                'ordering': ['-withdrawal_at'],
                'abstract': False,
            },
        ),
    ]
