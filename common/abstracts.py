from django.db import models
from django.contrib.admin import SimpleListFilter
from django.utils import timezone


from .managers import SoftDeleteManager




class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Skapad')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Senast ändrad')

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    deleted = models.BooleanField(default=False, null=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def hard_delete(self):
        super(SoftDeleteModel, self).delete()

    def restore(self):
        self.deleted = False
        self.deleted_at = None
        self.save()

    def delete(self, deleted_at=None):
        if deleted_at:
            self.deleted_at = deleted_at
        else:
            self.deleted_at = timezone.now()
        self.deleted = True
        self.save()


class SoftDeleteFilter(SimpleListFilter):
    title = 'deleted'
    parameter_name = 'deleted'

    def lookups(self, request, model_admin):
        return (('deleted', ('Deleted')), ('not_deleted', 'Not deleted'),)

    def queryset(self, request, queryset):
        if self.value() == 'deleted':
            return queryset.filter(deleted=True)
        elif self.value() == 'not_deleted':
            return queryset.filter(deleted=False)
        else:
            return queryset