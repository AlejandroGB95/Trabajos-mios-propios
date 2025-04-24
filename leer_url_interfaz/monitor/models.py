from django.db import models

class UrlMonitor(models.Model):
    url = models.URLField()
    hash = models.CharField(max_length=64, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    has_changed = models.BooleanField(default=False)
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        return self.url
