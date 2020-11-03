"""AnDjo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
# from django.contrib.auth import views as auth_views
from posts.views import search
from . import views
from .views import contacto
# from clients import views
# from .views import indexBlog, blog, post

# from admUsrsReg import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view()),
    path('servicios/', views.ServiciosView.as_view()),
    path('servicios/acupuntura', views.AcupunturaView.as_view(), name='acupuntura'),
    path('servicios/quiropractica', views.QuiropracticaView.as_view(), name='quiropractica'),
    path('servicios/psicologia', views.PsicologiaView.as_view(), name='psicologia'),
    path('servicios/rehabilitacion', views.RehabilitacionView.as_view(), name='rehabilitacion'),
    path('nosotros/', views.NosotrosView.as_view()),
    path('contacto/', contacto, name='contacto'),
    # path('contacto/', views.ContactoView.as_view()),
    path('blog/', include('posts.urls')),
    path('search/', search, name='search'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    path('gest/', include('gestion.urls')),
    path('accounting/', include('accounting.urls')), 
    # path('gest/', BlogListView.as_view(), name='BlogList'),
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login', kwargs={'next_page':'blog/'}),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout', kwargs={'next_page':'blog/'}),
    # path('caja/',views.addNewUsuario,name='caja'),
    # path('admUsrsReg/',include('admUsrsReg.urls')),
    # path('blog/', indexBlog),
    # path('blog/entradas', blog),
    # path('blog/post', post),
    # path('usuariosAnd/',include('usuariosAnd.urls',namespace='usuariosAnd')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
