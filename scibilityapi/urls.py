from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('projetos/', views.project_list),
    path('projetos/<int:id>/', views.project_detail),    
]