
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('<id>/<int:definition>/<aggregation>/<start_date>/<stop_date>/', views.detail, name='detail'),
    path('<id>/', views.detail, name='detail'),
]
