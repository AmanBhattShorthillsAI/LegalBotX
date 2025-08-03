from django.urls import path
from .views import SCNUploadView, AskQuestionAPI

urlpatterns = [
    path('upload/', SCNUploadView.as_view(), name='scn-upload'),
    path("ask/", AskQuestionAPI.as_view(), name="ask-question"),
]
