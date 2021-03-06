# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-01-09 09:42
from __future__ import unicode_literals

from django.db import migrations, models
import pyas2.models


class Migration(migrations.Migration):

    dependencies = [
        ('pyas2', '0017_auto_20170404_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='https_ca_cert',
            field=models.FileField(blank=True, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name='HTTPS Local CA Store'),
        ),
        migrations.AlterField(
            model_name='privatecertificate',
            name='ca_cert',
            field=models.FileField(blank=True, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name='Local CA Store'),
        ),
        migrations.AlterField(
            model_name='privatecertificate',
            name='certificate',
            field=models.FileField(upload_to=pyas2.models.get_certificate_path),
        ),
        migrations.AlterField(
            model_name='publiccertificate',
            name='ca_cert',
            field=models.FileField(blank=True, null=True, upload_to=pyas2.models.get_certificate_path, verbose_name='Local CA Store'),
        ),
        migrations.AlterField(
            model_name='publiccertificate',
            name='certificate',
            field=models.FileField(upload_to=pyas2.models.get_certificate_path),
        ),
    ]
