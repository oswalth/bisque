from django.contrib import admin

from data_access.flats.models import Address, Residential, Building, Flat


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Residential)
class ResidentialAdmin(admin.ModelAdmin):
    pass


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    pass


@admin.register(Flat)
class FlatAdmin(admin.ModelAdmin):
    pass
