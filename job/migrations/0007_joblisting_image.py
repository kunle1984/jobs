# Generated by Django 4.2.4 on 2023-08-15 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0006_joblisting_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='joblisting',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='job_image/'),
        ),
    ]