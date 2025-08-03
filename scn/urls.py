from django.urls import path
from .views import SCNUploadView

urlpatterns = [
    path('upload/', SCNUploadView.as_view(), name='scn-upload'),
]
