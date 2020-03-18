import hashlib
import random

from django.db import models


class GUIDModel(models.Model):
    """Base GUID model"""
    guid = models.CharField(db_column='guid', primary_key=True, max_length=40, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Save the GUIDModel, setting self.guid if not set"""
        if not self.guid:
            self.guid = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        """Unicode representation of this GUIDModel object"""
        return self.guid

