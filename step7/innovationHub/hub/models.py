from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse


def is_esprit_email(value):
    """
    Tests if An Email Ends with @esprit.tn
    """
    if not str(value).endswith("@esprit.tn"):
        raise ValidationError('Votre Email doit être @Esprit.tn', params={'value': value})


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # Ce champs sera modifié à la création
    updated_at = models.DateTimeField(auto_now=True)  # modifier pour chaque update

    # Rajouter les meta donnée à notre class
    class Meta:
        abstract = True  # pour dire que cette classe est une classe abstraite
        # et pour dire que cette classe on ne la considère pas comme etant
        # un modele c'est juste une classe utilitaure a fin d'éviter de dupliquer le code
        # classe abstraite=classe qu'on ne peut pas instancier


class User(models.Model):
    lastName = models.CharField('Prenom', max_length=30)
    firstName = models.CharField('Nom', max_length=30)
    email = models.EmailField('Email', validators=[is_esprit_email], null=False)

    def __str__(self):
        return ('nom: {} -- prenom: {}').format(self.lastName, self.firstName)


class Student(User):
    def get_absolute_url(self):
        return reverse('studentsLV')


class Coach(User):
    pass


class Project(models.Model):
    projectName = models.CharField('Titre du projet', max_length=30)
    projectDuration = models.IntegerField('Duree estimee', default=0)
    timeAllocated = models.IntegerField('Temps alloue',
                                        validators=[MinValueValidator(1), MaxValueValidator(10)])
    needs = models.TextField(max_length=250)
    description = models.TextField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)  # Ce champs sera modifié à la création
    updated_at = models.DateTimeField(auto_now=True)  # modifier pour chaque update

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

    def total_allocated_by_members(self):
        list_members_in_p = MembershipInProject.objects.filter(project=self.pk)
        sum_invested_by_members = list_members_in_p.all().aggregate(Sum('time_allocated_by_member'))
        # Utiliser Aggregate pour regroupe les valeurs à aggrégé dans un dictionnaire
        return sum_invested_by_members['time_allocated_by_member__sum'] or 0
        # Récupération de la valeur à partir du dictionnnaire

    def get_related_members(self):
        return self.members.all()

    def __str__(self):
        return self.projectName

    def get_absolute_url(self):
        return reverse('projectDV', kwargs={'pk': self.pk})


class MembershipInProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    time_allocated_by_member = models.IntegerField('Temps alloué par le membre')

    def __str__(self):
        return 'Member: {} | Project: {} '.format(self.student.lastName, self.project.projectName)

    class Meta:
        unique_together = ("project", "student")
