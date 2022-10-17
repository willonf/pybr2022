from django.contrib import admin
from basic import models


# TODO: Páginas que serão montadas no Django Admin

@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'modified_at']
    list_display_links = ['id', 'name', 'active', 'created_at', 'modified_at']
    search_fields = ['id', 'name']
    list_filter = ['active', 'name']
    # Outros campos podem ser adicionados


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'created_at', 'modified_at']
    list_display_links = ['id', 'name', 'active', 'created_at', 'modified_at']
    search_fields = ['id', 'name']
    list_filter = ['active', 'name']


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'salary', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'gender',
                          'salary', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'modified_at', 'active', 'employee', 'branch']
    list_display_links = ['id', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'modified_at', 'active', 'sale', 'product', 'quantity']
    list_display_links = ['id', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'abbreviation', 'modified_at', 'active']
    list_display_links = ['id', 'name',
                          'abbreviation', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']


@admin.register(models.Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'modified_at', 'active']
    list_display_links = ['id', 'name', 'modified_at', 'active']
    search_fields = ['name']
    list_filter = ['active']
