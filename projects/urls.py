from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('create/', views.create_project, name='create_project'),
    # path('search/', views.search_projects, name='search_projects'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
