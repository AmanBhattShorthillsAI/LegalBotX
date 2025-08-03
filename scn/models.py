from django.db import models

# Create your models here.
class SCNUpload(models.Model):
    file = models.FileField(upload_to="scns/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
