# Generated by Django 3.2.5 on 2021-07-20 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliance',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='Total'),
        ),
        migrations.AddField(
            model_name='redeem',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='Total'),
        ),
        migrations.AlterField(
            model_name='appliance',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Unit Price'),
        ),
        migrations.AlterField(
            model_name='appliance',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='redeem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, max_digits=11, verbose_name='Unit Price'),
        ),
        migrations.AlterField(
            model_name='redeem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
    ]
