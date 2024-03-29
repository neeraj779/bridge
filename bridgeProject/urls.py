"""bridgeProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from bridge import views

urlpatterns = [
    path('bridge/admin/', admin.site.urls),
    path('', views.landingPage, name='landingPage'),
    path('bridge/', include('bridge.urls')),
    path('bridge/auth/', include('authentication.urls')),
    path('bridge/accounts/', include("django.contrib.auth.urls")),
]

# error handler for 404 and 500
handler404 = 'bridge.views.error_404'
handler500 = 'bridge.views.error_500'