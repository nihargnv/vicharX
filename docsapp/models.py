# from django.db import models
# # from storages.backends.gcloud import GoogleCloudStorage

# # storage = GoogleCloudStorage()

# class Document(models.Model):
#     title = models.CharField(max_length=255)
#     file = models.FileField(storage=storage, upload_to="documents/")
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     category = models.CharField(max_length=50, default="unknown")
#     summary = models.TextField()


from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to="documents/")  # Store in 'media/documents/'
    category = models.CharField(max_length=50, default="unknown")
    summary = models.TextField()
    metadata = models.JSONField()

    def __str__(self):
        return self.file.name[10:]  # Show filename in Django Admin