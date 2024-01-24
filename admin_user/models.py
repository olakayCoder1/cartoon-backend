from django.db import models
from uuid import uuid4

# Create your models here.



class FAQ(models.Model):
    uuid = models.CharField(max_length=100 , unique=True)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_featured = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        # Generate a new unique uuid if it's not set
        if not self.uuid:
            self.uuid = str(uuid4())

        super().save(*args, **kwargs)


    
    def serialized_user_data(self):
        data = dict(
            id=self.uuid,
            question=self.question,
            answer=self.answer,
            is_featured=self.is_featured,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
        return data