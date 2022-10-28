import uuid

from django.db import models
from django.utils import timezone


class UidMixin(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        abstract = True


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = "updated_at"
        abstract = True


class ArchivedAtMixin(models.Model):
    archived_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def archive(self) -> None:
        self.archived_at = timezone.now()
        self.save()

    @property
    def is_archived(self) -> bool:
        return self.archived_at is not None


class BaseModel(CreatedAtMixin, UpdatedAtMixin):
    class Meta:
        abstract = True


class BaseUidModel(UidMixin, CreatedAtMixin, UpdatedAtMixin):
    class Meta:
        abstract = True
