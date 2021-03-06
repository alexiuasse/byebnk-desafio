from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from .serializers import *
from .utils import get_client_ip, FinancialMixin


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rest_add_asset(request):
    """Adiciona um ativo depois de validado."""
    asset_serializer = AssetAddSerializer(data=request.data)
    # se não for válido, então vai lançar uma exceção
    if asset_serializer.is_valid(raise_exception=True):
        asset = asset_serializer.save()
        return Response(asset_serializer.data, status=HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rest_list_asset(request):
    """
    Retorna uma lista de ativos com possibilidade de query pela modalidade.
    """
    modality_query = request.GET.get('modality', None)
    if modality_query is not None:
        asset = Asset.objects.filter(modality=modality_query)
    else:
        asset = Asset.objects.all()
    asset_serializer = AssetGetSerializer(asset, many=True)
    return Response(asset_serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rest_appliance_list(request):
    """Retorna uma lista de aplicações pertencentes ao usuário da requisição."""
    appliance_serializer = ApplianceGetSerializer(
        Appliance.objects.filter(user=request.user),
        many=True
    )
    return Response(appliance_serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rest_appliance_add(request):
    """Cria uma aplicação e adiciona o endereço de ip."""
    # transformando a criação em atômica
    with transaction.atomic():
        data = request.data.copy()
        data['ip_address'] = get_client_ip(request)
        appliance_serializer = ApplianceAddSerializer(data=data)
        if appliance_serializer.is_valid(raise_exception=True):
            appliance = appliance_serializer.save()
            return Response(appliance_serializer.data, status=HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rest_redeem_add(request):
    """Cria um resgate e adiciona o endereço de ip."""
    # transformando a criação em atômica
    with transaction.atomic():
        data = request.data.copy()
        data['ip_address'] = get_client_ip(request)
        redeem_serializer = RedeemAddSerializer(data=data)
        if redeem_serializer.is_valid(raise_exception=True):
            redeem = redeem_serializer.save()
            return Response(redeem_serializer.data, status=HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rest_redeem_list(request):
    """Retorna a lista de resgates pertencentes ao usuário da requisição."""
    redeem_serializer = RedeemGetSerializer(
        Redeem.objects.filter(user=request.user),
        many=True
    )
    return Response(redeem_serializer.data, status=HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_appliance_data_chart_donut(request):
    """Retorna dados para preencher um gráfico de pizza."""
    financialMixin = FinancialMixin(request)
    return Response(financialMixin.get_appliance_by_asset_donut_chart())
