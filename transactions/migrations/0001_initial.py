# Generated by Django 4.0.8 on 2022-10-16 15:53

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_alter_account_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('is_active', models.BooleanField(default=True, help_text='Object status.')),
                ('name', models.CharField(max_length=120, verbose_name=' name')),
                ('description', models.CharField(max_length=120)),
                ('category', models.CharField(choices=[('Food', 'Food'), ('Gas', 'Gas'), ('Investment', 'Investment'), ('Other', 'Other'), ('Entertainment', 'Entertainment'), ('Insurance', 'Insurance'), ('Groceries', 'Groceries'), ('Gaming', 'Gaming'), ('Education', 'Education'), ('Fashion', 'Fashion'), ('Transport', 'Transport'), ('Personal', 'Personal'), ('Housing', 'Housing'), ('Debt', 'Debt'), ('Rent', 'Rent'), ('Salaries', 'Salaries'), ('Income', 'Income'), ('Time job', 'Time job'), ('Bonus', 'Bonus'), ('Wage', 'Wage'), ('Tip', 'Tip')], max_length=20)),
                ('amount', models.FloatField(default=0, help_text='Balance summary from account.', verbose_name='transaction amount')),
                ('type', models.CharField(choices=[('Income', 'Income'), ('Expense', 'Expense')], max_length=20)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='accounts.account')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MonthlyBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, help_text='Date time on which the object was created.', verbose_name='created at')),
                ('modified', models.DateField(auto_now=True, help_text='Date time on which the object was last modified.', verbose_name='modified at')),
                ('is_active', models.BooleanField(default=True, help_text='Object status.')),
                ('billing_date', models.IntegerField(validators=[django.core.validators.MaxValueValidator(30), django.core.validators.MinValueValidator(1)])),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='transactions.transaction')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]
