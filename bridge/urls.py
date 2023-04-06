from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='bridge-home'),
    path('text-to-speech/', views.tts, name='tts'),
    path('speech-text-to/', views.stt, name='stt'),
    path('pdf-reader/', views.pts, name='pts'),
    path('associates/', views.associates, name='associates'),
    path('remove_associates/', views.removeassociates, name='removeassociates'),
    path('download_file/<str:doc_name>/', views.download_file, name='download_file'),
    path('upload_file/', views.uploadFile, name='uploadFile'),
    path('preview/', views.preview, name='preview'),
    path('upload/', views.upload_files, name='upload'),
    path('check_doc/<str:file_name>/', views.check_doc, name='check_doc'),
    path('save_data/<str:doc_name>/<int:no_of_pages>/<str:github_username>/<str:model>/<str:file>/', views.save_data, name='save_data'),
    path('demo/', views.landingPage, name='landingPage'),
]