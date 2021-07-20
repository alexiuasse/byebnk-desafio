from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from .models import *
from .serializers import *


class TestAsset(TestCase):

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

    def test_asset_rest_api_list_sorted(self):
        """
        Testar a api rest está enviando lista filtrada de ativos corretamente.
        """
        response = self.client.get(
            '/financial/api/rest/asset/list/?modality=RF'
        )
        self.assertEqual(response.status_code, 200)

        asset = Asset.objects.filter(modality="RF")
        asset_serializer = AssetGetSerializer(data=asset, many=True)
        asset_serializer.is_valid()
        self.assertListEqual(
            response.data,
            asset_serializer.data,
        )


class TestAppliance(TestCase):

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

    def test_rest_appliance_add(self):
        """Testar criação de aplicação no rest api."""
        response = self.client.post(
            '/financial/api/rest/appliance/add/',
            data={
                'asset': 1,
                'request_date': timezone.now().date(),
                'quantity': 1,
                'unit_price': 10,
                'user': 1,
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_rest_appliance_ip(self):
        """Testar o ip adicionado a cada aplicação."""
        response = self.client.post(
            '/financial/api/rest/appliance/add/',
            data={
                'asset': 1,
                'request_date': timezone.now().date(),
                'quantity': 1,
                'unit_price': 10,
                'user': 1,
            }
        )
        self.assertEqual(response.data['ip_address'], '127.0.0.1')


class TestRedeem(TestCase):

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

    def test_rest_appliance_add(self):
        """Testar criação de retirada no rest api."""
        response = self.client.post(
            '/financial/api/rest/redeem/add/',
            data={
                'asset': 1,
                'request_date': timezone.now().date(),
                'quantity': 1,
                'unit_price': 10,
                'user': 1,
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_rest_appliance_ip(self):
        """Testar o ip adicionado a cada retirada."""
        response = self.client.post(
            '/financial/api/rest/redeem/add/',
            data={
                'asset': 1,
                'request_date': timezone.now().date(),
                'quantity': 1,
                'unit_price': 10,
                'user': 1,
            }
        )
        self.assertEqual(response.data['ip_address'], '127.0.0.1')
