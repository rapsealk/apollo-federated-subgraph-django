from uuid import uuid4

from django.db import models


class Job(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, null=False, default=uuid4)
