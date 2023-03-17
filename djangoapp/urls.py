"""djangoapp URL Configuration

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
from django.urls import path
from task import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('task/', views.task, name='tasks'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('signin/', views.signin, name='signin'),
    path('task/create', views.create_task, name='create_task'),
    path('task/detail/<int:task_id>', views.task_detail, name='task_detail'),
    path('task/complete/<int:task_id>', views.task_complete, name='task_complete'),
    path('task/uncomplete/<int:task_id>', views.task_incomplete, name='task_incomplete'),
    path('task/delete/<int:task_id>', views.task_delete, name='task_delete'),
]
