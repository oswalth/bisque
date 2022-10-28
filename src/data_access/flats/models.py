from autoslug import AutoSlugField
from django.db import models

from data_access.mixins import BaseModel, BaseUidModel


class Address(BaseUidModel):
    class Meta:
        app_label = "flats"
        db_table = "addresses"

    region = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    district = models.CharField(max_length=128, null=True, blank=True)
    street = models.CharField(max_length=256)
    street_number = models.CharField(max_length=16)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=10, decimal_places=8)

    def __str__(self):
        return f"{self.city}, {self.street}, {self.street_number}"


class Residential(BaseUidModel):
    class Meta:
        app_label = "flats"
        db_table = "residentials"

    name = models.CharField(
        max_length=256
    )
    slug = AutoSlugField(
        max_length=256,
        unique=True,
        populate_from="name",
    )

    def __str__(self):
        return self.name


class Building(BaseUidModel):
    class Meta:
        app_label = "flats"
        db_table = "flat"

    residential = models.ForeignKey(
        to=Residential,
        on_delete=models.CASCADE,
        db_column="residential_uid",
        related_name="buildings",
        related_query_name="building",
        null=True,
        blank=True,
    )
    address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        db_column="address_uid",
        related_name="buildings",
        related_query_name="building",
    )
    build_year = models.IntegerField()
    total_floors = models.IntegerField()


class Flat(BaseModel):
    class Meta:
        app_label = "flats"
        db_table = "flats"

    rooms = models.IntegerField()
    total_area = models.DecimalField(max_digits=7, decimal_places=2)
    living_area = models.DecimalField(max_digits=7, decimal_places=2)
    kitchen_area = models.DecimalField(max_digits=7, decimal_places=2)
    floor = models.IntegerField()
    flat_number = models.CharField(max_length=8)
    building = models.ForeignKey(
        to=Building,
        on_delete=models.CASCADE,
        db_column="residential_uid",
        related_name="buildings",
        related_query_name="building",
    )
