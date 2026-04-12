from django.db import models

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