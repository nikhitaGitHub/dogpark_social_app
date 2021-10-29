# Generated by Django 2.1.5 on 2021-10-28 15:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dogpark', '0006_friendship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateField(blank=True, default=datetime.date.today, null=True)),
                ('time', models.TimeField()),
                ('attending', models.BooleanField(default=False)),
                ('attended', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Goals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=256)),
                ('pointsEarned', models.IntegerField(default=0)),
                ('addGoal', models.BooleanField(default=False)),
                ('completeGoal', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='the_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='from_friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_friend', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendship',
            name='to_friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_friend', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together={('sender', 'receiver')},
        ),
        migrations.AlterUniqueTogether(
            name='friendship',
            unique_together={('from_friend', 'to_friend')},
        ),
    ]
