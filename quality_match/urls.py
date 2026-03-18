from django.urls import path
from .views import  quality_match_page, quality_match_api,  quality_camera_view

urlpatterns = [
    path("match/", quality_match_page, name="quality_match_page"),
    path("match/api/", quality_match_api, name="quality_match_api"),
    path("camera/", quality_camera_view, name="quality_camera"),
]
