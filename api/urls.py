from rest_framework import routers
from .views import ProductView

router = routers.SimpleRouter()
router.register(r'products', ProductView)

urlpatterns = [

]


urlpatterns += router.urls