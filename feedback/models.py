from django.db import models

class Feedback(models.Model):
    message = models.TextField()
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=15)
    media_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.sender_email}"
