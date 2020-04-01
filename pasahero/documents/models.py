import os
from django.db import models
from .validator import file_size
from commuters.models import Commuters

class Documents(models.Model):
    commuter_id = models.ForeignKey(Commuters, related_name="documents", on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    document = models.FileField(upload_to='commuter_documents/', validators=[file_size])

    def file_type(self):
        name, extension = os.path.splitext(self.document.name)
        if extension == '.pdf':
            return 'pdf'
        return 'other'