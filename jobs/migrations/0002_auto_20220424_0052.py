# Generated by Django 3.2.2 on 2022-04-23 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20220424_0052'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='applicantscount',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='jobs',
            name='career_level',
            field=models.CharField(default='Junior', max_length=20),
        ),
        migrations.AddField(
            model_name='jobs',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='applicants',
            field=models.ManyToManyField(blank=True, to='account.Profile'),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='education_level',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='jobs',
            name='salary',
            field=models.CharField(max_length=10, null=True),
        ),
    ]