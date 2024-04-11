from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('projetos', views.ProjetoViewSet)
# router.register('habilidades', views.HabilidadeViewSet)

projetos_router = routers.NestedDefaultRouter(router, 'projetos', lookup='projeto')
projetos_router.register('habilidades', views.HabilidadeViewSet, basename='projeto-habilidades')



# URLConf
urlpatterns = router.urls + projetos_router.urls