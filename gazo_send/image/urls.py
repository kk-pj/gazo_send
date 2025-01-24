from django.urls import path
from . import views

app_name = 'image'

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('complete/', views.complete, name='complete'),  # 完了画面
    path('list/', views.list_images, name='list_images'),
    path('download/<int:image_id>/', views.download_image, name='download_image'),
    path('download/', views.download_images_in_range, name='download_images_in_range'),
]