# Generated by Django 3.2.2 on 2022-05-08 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20220424_0052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='specialities',
        ),
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='accountcode',
            name='verification_code',
            field=models.CharField(max_length=6),
        ),
    ]
