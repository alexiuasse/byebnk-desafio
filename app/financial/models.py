from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class Asset(models.Model):
    """Ativos."""

    RENDA_FIXA = "RF"
    RENDA_VARIAVEL = "RV"
    CRIPTO = "CR"

    MODALITY_CHOICES = [
        (RENDA_FIXA, 'Renda Fixa'),
        (RENDA_VARIAVEL, 'Renda Variável'),
        (CRIPTO, 'Cripto'),
    ]

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=128
    )
    modality = models.CharField(
        verbose_name=_("Modality"),
        choices=MODALITY_CHOICES,
        max_length=2,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        """Capitalize the name."""
        self.name = self.name.capitalize()
        super(Asset, self).save(*args, **kwargs)


class BaseFinancial(models.Model):
    """Modelo de base para aplicações (Appliance) e retiradas (Redeem)."""

    asset = models.ForeignKey(
        "financial.Asset",
        verbose_name=_("Modality"),
        on_delete=models.CASCADE
    )
    request_date = models.DateField(
        verbose_name=_("Request Date")
    )
    quantity = models.IntegerField(
        verbose_name=_("Quantity")
    )
    unit_price = models.DecimalField(
        verbose_name=_("Value"),
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField()

    class Meta:
        abstract = True


class Appliance(BaseFinancial):
    """Aplicações."""


class Redeem(BaseFinancial):
    """Resgates."""
