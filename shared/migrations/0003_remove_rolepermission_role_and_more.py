# Generated by Django 5.1.5 on 2025-01-22 02:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('shared', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rolepermission',
            name='role',
        ),
        migrations.RemoveField(
            model_name='rolepermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='commission',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_method',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='tax',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='payment',
            name='method',
            field=models.CharField(choices=[('CASH', 'Cash'), ('CARD', 'Credit/Debit Card'), ('ONLINE', 'Online Payment')], default='credit_card', max_length=20),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='AppModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('app_label', models.CharField(help_text="The app label this module belongs to (e.g., 'shared', 'users')", max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_full_app', models.BooleanField(default=False, help_text='Check if this represents the entire app')),
                ('permissions', models.ManyToManyField(blank=True, related_name='app_modules', to='auth.permission')),
            ],
            options={
                'verbose_name': 'App Module',
                'verbose_name_plural': 'App Modules',
            },
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='RolePermission',
        ),
    ]
