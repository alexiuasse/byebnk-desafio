from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from .serializers import *


# Eu poderia ter usado a classe ModelViewSet disponível no django restframework
# porém como essa parte da api é para somente criar um ativo (asset) é mais
# simples fazer dessa forma.

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rest_add_asset(request):
    # definindo o usuário que criou como o usuário da requisição, caso não seja enviado pelo aplicativo
    # data = request.data.copy()
    # data['user'] = request.user
    asset_serializer = AssetAddSerializer(data=request.data)
    # se não for válido, então vai lançar uma exceção
    if asset_serializer.is_valid(raise_exception=True):
        asset = asset_serializer.save()
        return Response(asset_serializer.data, status=HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rest_list_asset(request):
    asset_serializer = AssetGetSerializer(Asset.objects.all(), many=True)
    return Response(asset_serializer.data, status=HTTP_200_OK)
