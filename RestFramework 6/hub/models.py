from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Project(models.Model):
    project_name = models.CharField('Project Title', max_length=30)
    duration = models.IntegerField('Duration', default=0)
    allocated_time = models.IntegerField(
        'Allocated time', validators=[MinValueValidator(1), MaxValueValidator(10)])
    needs = models.TextField(max_length=250)
    description = models.TextField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_valid = models.BooleanField(default=False)

    creator = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='project_owner', blank=True
                                )
