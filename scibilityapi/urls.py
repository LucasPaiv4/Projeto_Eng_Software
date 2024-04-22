from django.urls import path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('projetos', views.ProjetoViewSet)
router.register('usuarios', views.UsuarioViewSet)
router.register('interesses', views.InteresseProjetoViewSet, basename='interesses')
#router.register('usuarios/me/habilidades', views.HabilidadeUsuarioViewSet, basename='habilidades-usuario')
# router.register('habilidades', views.HabilidadeViewSet)

projetos_router = routers.NestedDefaultRouter(router, 'projetos', lookup='projeto')
projetos_router.register('habilidades', views.HabilidadeViewSet, basename='projeto-habilidades')

usuarios_router = routers.NestedDefaultRouter(router, 'usuarios', lookup='usuario')
usuarios_router.register('habilidades', views.HabilidadeUsuarioViewSet, basename='usuario-habilidades')



# URLConf
urlpatterns = router.urls + projetos_router.urls + usuarios_router.urls