from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse


class User(models.Model):
    lastName = models.CharField('Prenom', max_length=30)
    firstName = models.CharField('Nom', max_length=30)
    email = models.EmailField('Email', null=False)

    def __str__(self):
        return 'nom: {} -- prenom: {}'.format(self.lastName, self.firstName)


class Student(User):
    pass


class Coach(User):
    pass


class Project(models.Model):
    projectName = models.CharField('Titre du projet', max_length=30)
    projectDuration = models.IntegerField('Duree estimee', default=0)
    timeAllocated = models.IntegerField('Temps alloue')
    needs = models.TextField(max_length=250)
    description = models.TextField(max_length=250)

    # Validation State of the project
    isValid = models.BooleanField(default=False)

    creator = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name='project_owner'
    )

    supervisor = models.ForeignKey(
        Coach,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='project_coach'
    )

    members = models.ManyToManyField(
        Student,
        through='MembershipInProject',
        # added to differ with the lead relation
        related_name='les_membres',
        blank=True,
    )

    def __str__(self):
        return self.projectName


class MembershipInProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time_allocated_by_member = models.IntegerField('Temps alloué par le membre')

    def __str__(self):
        return 'Member: {} | Project: {} '.format(self.student.lastName, self.project.projectName)

    class Meta:
        unique_together = ("project", "student")
