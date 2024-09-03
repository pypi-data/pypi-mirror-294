from django.db import models
from .mixins.models import AbstractBaseModel


class DBTimerHistory(AbstractBaseModel):

    html_file = models.FileField(
        "processed as HTML",
        blank=True,
        null=True,
        help_text="Processed HTML rendering.",
    )
    
    class Meta:
        ordering = ("created_at",)
        
class DBTimerHelper(AbstractBaseModel):
    
    json_file = models.FileField(
        "processed",
        blank=True,
        null=True,
        help_text="Processed JSON rendering.",
    )
    
    master = models.ForeignKey(
        DBTimerHistory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    
    class Meta:
        ordering = ("created_at",)