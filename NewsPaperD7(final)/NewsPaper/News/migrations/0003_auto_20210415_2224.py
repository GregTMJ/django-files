# Generated by Django 3.2 on 2021-04-15 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('News', '0002_auto_20210415_2208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='News.category'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]