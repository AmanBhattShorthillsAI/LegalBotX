from rest_framework import serializers
from .models import SCNUpload

class SCNUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SCNUpload
        fields = ['id', 'file', 'uploaded_at']
