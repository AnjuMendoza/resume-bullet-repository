from django.conf import settings
from django.db import models


class ResumeSection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resume_sections')
    name = models.CharField(max_length=120)
    notes = models.TextField(blank=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position', 'created_at']

    def __str__(self):
        return self.name


class Bullet(models.Model):
    CATEGORY_CHOICES = [
        ('work', 'Work Experience'),
        ('project', 'Projects'),
        ('education', 'Education'),
        ('skills', 'Skills and Qualifications'),
        ('volunteer', 'Volunteer Experience'),
    ]

    text = models.TextField()
    main_category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=100)
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
