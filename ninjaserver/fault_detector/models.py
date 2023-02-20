from django.db import models

# Create your models here.
class EventSignal(models.Model):
    title = models.CharField(max_length=250)
    CSV = models.FileField(upload_to="fault_detector/csv_samples")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title)
    