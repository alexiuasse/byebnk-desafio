from django.db.models import fields
from rest_framework import serializers

from .models import *


class AssetAddSerializer(serializers.ModelSerializer):

    def validate(self, data):
        assets_count = Asset.objects.filter(
            name=data['name'].capitalize()
        ).count()
        if assets_count > 0:
            raise serializers.ValidationError(
                "Já existe um Ativo com esse nome."
            )
        return data

    class Meta:
        model = Asset
        fields = ['pk', 'name', 'modality', 'user']


class AssetGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ['pk', 'name', 'modality']


class ApplianceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appliance
        fields = ['asset', 'request_date', 'quantity', 'unit_price']


class RedeemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Redeem
        fields = ['asset', 'request_date', 'quantity', 'unit_price']
