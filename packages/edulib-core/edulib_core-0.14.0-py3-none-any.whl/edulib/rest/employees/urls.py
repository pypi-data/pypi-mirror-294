from rest_framework.routers import (
    SimpleRouter,
)

from edulib.rest.employees.views import (
    EmployeeViewSet,
)


router = SimpleRouter()

router.register('employees', EmployeeViewSet, basename='employees')
