from django.urls import path

from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_listing, name='job_listing'),
    path('create/', views.create_job, name='create_job'),

]