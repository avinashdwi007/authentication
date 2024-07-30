
from django.urls import path,include
from app2 import views
from rest_framework import routers
from .views import BlogViewSet
router = routers.DefaultRouter()
router.register(r'newblog', BlogViewSet, basename='blog')

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('', views.index, name='home'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('blog', views.blog, name='blog'),
    path('post', views.post, name='post'),
    path('blogpost/', include(router.urls)), 
]