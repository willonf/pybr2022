from rest_framework.routers import DefaultRouter
from basic import viewsets

router = DefaultRouter()
router.register('branch', viewsets.BranchViewSet)
router.register('city', viewsets.CityViewSet)
router.register('customer', viewsets.CustomerViewSet)
router.register('department', viewsets.DepartmentViewSet)
router.register('district', viewsets.DistrictViewSet)
router.register('employee', viewsets.EmployeeViewSet)
router.register('marital_status', viewsets.MaritalStatusViewSet)
router.register('product', viewsets.ProductViewSet)
router.register('product_group', viewsets.ProductGroupViewSet)
router.register('sale', viewsets.SaleViewSet)
router.register('sale_item', viewsets.SaleItemViewSet)
router.register('supplier', viewsets.SupplierViewSet)
router.register('state', viewsets.StateViewSet)
router.register('zone', viewsets.ZoneViewSet)

urlpatterns = router.urls
