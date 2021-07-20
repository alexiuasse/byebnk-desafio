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


class ApplianceAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appliance
        fields = ['asset', 'request_date',
                  'quantity', 'unit_price', 'user', 'ip_address']


class ApplianceGetSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Appliance
        fields = ['asset', 'request_date', 'quantity', 'unit_price', 'user']


class RedeemAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Redeem
        fields = ['asset', 'request_date',
                  'quantity', 'unit_price', 'user', 'ip_address']


class RedeemGetSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Redeem
        fields = ['asset', 'request_date', 'quantity', 'unit_price', 'user']
