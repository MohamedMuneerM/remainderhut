# Generated by Django 3.2.9 on 2021-11-15 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemainderTasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=999)),
                ('remainder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.remainder')),
            ],
        ),
    ]
