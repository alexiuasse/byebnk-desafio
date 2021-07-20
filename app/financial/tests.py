from django.test import TestCase
from django.contrib.auth.models import User

from .models import *
from .serializers import *


class TestAssetCreation(TestCase):

    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        # user.is_superuser = True
        user.save()
        self.client.login(username='testuser', password="12345")

        Asset.objects.create(
            name="BITCOIN",
            modality="RF",
            user=user,
        )

    def test_asset_name(self):
        """Testar se o nome está sendo corretamente criado."""
        asset = Asset.objects.get(name__icontains="Bitcoin")
        self.assertEqual("Bitcoin", asset.name)

    def test_asset_serializer_creation_same_name(self):
        """Testar se o serializer de criação com mesmo nome."""
        user = User.objects.get(pk=1)
        asset_serializer = AssetAddSerializer(
            data={
                'name': 'Bitcoin',
                'modality': 'RF',
                'user': user.pk,
            }
        )
        is_valid = asset_serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertEqual(
            "Já existe um Ativo com esse nome.",
            asset_serializer.errors['non_field_errors'][0]
        )

    def test_asset_rest_api_add(self):
        """Testar a api rest de criação de ativo."""
        user = User.objects.get(pk=1)
        response = self.client.post(
            '/financial/api/rest/asset/add/',
            data={
                'name': 'Fundos Imobiliários',
                'modality': 'RF',
                'user': user.pk,
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_asset_rest_api_list(self):
        """Testar a api rest está enviando lista de ativos corretamente."""
        response = self.client.get('/financial/api/rest/asset/list/')
        self.assertEqual(response.status_code, 200)

        asset_serializer = AssetGetSerializer(
            data=Asset.objects.all(),
            many=True
        )
        asset_serializer.is_valid()
        self.assertListEqual(
            response.data,
            asset_serializer.data,
        )
