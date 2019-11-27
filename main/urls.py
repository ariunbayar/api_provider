"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

import column.views
import notification.views
import pages.views
import record.views
import request.views
import secure.views
import table.views


urlpatterns = [

    path('login/', secure.views.login, name='login'),
    path('logout/', secure.views.logout, name='logout'),

    path('p/css-guide/', pages.views.css_guide, name='css-guide'),

    path('table/', table.views.list, name='table-list'),
    path('table/new/', table.views.new, name='table-new'),
    path('table/<int:pk>/', table.views.detail, name='table-detail'),
    path('table/<int:pk>/edit/', table.views.edit, name='table-edit'),
    path('table/<int:pk>/delete/', table.views.delete, name='table-delete'),

    path('table/<int:table_pk>/new/', column.views.new, name='column-new'),
    path('table/<int:table_pk>/<int:pk>/edit/', column.views.edit, name='column-edit'),
    path('table/<int:table_pk>/<int:pk>/delete/', column.views.delete, name='column-delete'),

    path('notification/mark-as-read/', notification.views.mark_as_read, name='notification-mark-as-read'),

    path('request/', request.views.list, name='request-list'),

    path('api/<str:table_name>/new/', record.views.insert, name='api-record-insert'),
    path('api/<str:table_name>/', record.views.fetch, name='api-record-fetch'),

]
