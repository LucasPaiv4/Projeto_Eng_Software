from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('projetos', views.ProjetoViewSet)
router.register('habilidades', views.HabilidadeViewSet)

# URLConf
urlpatterns = router.urls