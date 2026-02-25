from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.index, name="home"),
    path('flat', views.flat, name='flat'),
    path('news', views.news, name='news'),
    path('info', views.info, name='info'),
    path('filter', views.filter, name='filter_flat'),
    path('application', views.application, name="application"),
    path('flat/<int:pk>', views.NewFlat.as_view(), name='next_flat'),
    path('login/', views.register, name='login'),
    path('logout/', logout_view, name='logout'),
    path("api/process_xml/", views.process_xml),
]
