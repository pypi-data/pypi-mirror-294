from uuid import uuid4
from django.db import models

class ActiveManager(models.Manager):
    
    def active(self, *args, **kwargs):
        return self.filter(active=True)

class AbstractBaseModel(models.Model):
    """
    Abstract base model with datetime and UUID as primary key.
    """

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    objects = ActiveManager()

    class Meta:
        abstract = True