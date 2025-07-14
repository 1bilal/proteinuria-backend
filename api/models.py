from django.conf import settings
from django.db import models
from django.utils.timezone import now


class TestResult(models.Model):
    USER_INPUT = "manual"
    AUTO_DETECTED = "auto"

    ENTRY_METHOD_CHOICES = [
        (USER_INPUT, "Manual Entry"),
        (AUTO_DETECTED, "Auto Detected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result = models.CharField(max_length=10)  # e.g., Negative, Trace, +1, +2, +3
    image = models.ImageField(upload_to="test_images/", null=True, blank=True)
    entry_method = models.CharField(max_length=10, choices=ENTRY_METHOD_CHOICES)
    timestamp = models.DateTimeField(default=now)
    notes = models.TextField(blank=True, null=True)  # Optional notes field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} ({self.entry_method}) - {self.timestamp}"
