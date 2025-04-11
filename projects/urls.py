from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.create_project, name='create_project'),
    path('admin/', admin.site.urls),
    path('categories/<int:category_id>/', views.category_projects, name='category_projects'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)