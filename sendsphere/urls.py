from django.contrib import admin
from django.urls import include, path
import sys
sys.path.append('C:/lessons/SendSphere/SendSphere')
from newsletter import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newsletter/', include('newsletter.urls')),
    path('users/', include('users.urls')),
    path('', views.HomeView.as_view(), name='home'),

]
