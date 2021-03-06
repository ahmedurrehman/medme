from _ast import arg

import rest_framework
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from medme.models import Medicine, MedmeUser, Order
from medme.serializers import MedicineSerializer, OrderSerializer, UserSerializer, OrderByUserSerializer
from rest_framework import mixins, viewsets, filters


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'orders': reverse('order-list', request=request, format=format),
        'medicines': reverse('medicine-list', request=request, format=format),

    })


# class MedicineList(mixins.ListModelMixin,
#                    mixins.CreateModelMixin,
#                    generics.GenericAPIView):
#     queryset = Medicine.objects.all()
#     serializer_class = MedicineSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#

class MedicineViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MedicineSerializer
    queryset = Medicine.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name', '^company', '^generic_name')


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^customer__name','^customer__phone','^items__name')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = MedmeUser.objects.all()
    serializer_class = UserSerializer


class OrderByUserViewSet(viewsets.ModelViewSet):
    queryset = MedmeUser.objects.all()
    serializer_class = OrderByUserSerializer
