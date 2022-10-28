from dependency_injector.wiring import inject, Provide
from django.http import HttpRequest
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

from api.messaging.client import MessagingClient
from api.messaging.events import FlatEvent
from containers import Container
from data_access.flats.models import Flat, Building, Residential, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class ResidentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residential
        fields = "__all__"


class ResidentialViewSet(viewsets.ModelViewSet):
    queryset = Residential.objects.all()
    serializer_class = ResidentialSerializer


class BuildingSerializer(serializers.ModelSerializer):
    residential = ResidentialSerializer(read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Building
        fields = "__all__"


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer


class FlatSerializer(serializers.ModelSerializer):
    building = BuildingSerializer(read_only=True)

    class Meta:
        model = Flat
        fields = "__all__"


class FlatViewSet(viewsets.ModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer

    def get_queryset(self):
        queryset = self.queryset.prefetch_related(
            "building",
            "building__address",
            "building__residential"
        )
        return queryset

    @inject
    def create(
        self,
        request: HttpRequest,
        messaging_client: MessagingClient = Provide[Container.messaging_client],
        *args,
        **kwargs
    ):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        with messaging_client as mq:
            mq.send_flat_message(flat_id=serializer.data["id"], type_=FlatEvent.CREATE.value())
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @inject
    def update(
        self,
        request: HttpRequest,
        messaging_client: MessagingClient = Provide[Container.messaging_client],
        *args,
        **kwargs
    ):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        with messaging_client as mq:
            mq.send_flat_message(flat_id=serializer.data["id"], type_=FlatEvent.UPDATE.value())
        return Response(serializer.data)

    @inject
    def destroy(
        self,
        request: HttpRequest,
        messaging_client: MessagingClient = Provide[Container.messaging_client],
        *args,
        **kwargs
    ):
        instance = self.get_object()
        self.perform_destroy(instance)

        with messaging_client as mq:
            mq.send_flat_message(flat_id=instance.pk, type_=FlatEvent.DELETE.value)
        return Response(status=status.HTTP_204_NO_CONTENT)
