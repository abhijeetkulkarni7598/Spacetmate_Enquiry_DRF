from django.db import models
from app.models import UserAccount

# Create your models here.
class stepsModel(models.Model):
     # Choices for the steps field
    PROJECT_START = 'PROJECT_START'
    STRUCTURAL_WORK = 'STRUCTURAL_WORK'
    LAMINATE_WORK = 'LAMINATE_WORK'
    HARDWARE_INSTALL = 'HARDWARE_INSTALL'
    FURNISHING_WORK = 'FURNISHING_WORK'
    HAND_OVER_AND_FINALIZING = 'HAND_OVER_AND_FINALIZING'
    DONE = 'DONE'
    NOT_DONE = 'NOT_DONE'

    STEP_CHOICES = [
        (PROJECT_START, 'Project Start'),
        (STRUCTURAL_WORK, 'Structural Work'),
        (LAMINATE_WORK, 'Laminate Work'),
        (HARDWARE_INSTALL, 'Hardware Installation'),
        (FURNISHING_WORK, 'Furnishing Work'),
        (HAND_OVER_AND_FINALIZING, 'Hand Over and Finalizing'),
    ]
    DONE = [
        (DONE, 'DONE'),
        (NOT_DONE, 'NOT_DONE'),
   
    ]

    model_name = models.CharField(max_length = 50, choices=STEP_CHOICES, default=PROJECT_START)
    status = models.CharField (max_length = 50, choices=DONE, default=NOT_DONE)
    user = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f'{self.id}-{self.model_name}-{self.Status}'
    
class imgTitleStructuralWork(models.Model):
    title = models.CharField(max_length=100)
    img = models.FileField(upload_to='execution_work_images/')  # You might want to adjust the upload_to path
    stepsmodel = models.ForeignKey(stepsModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.stepsmodel}"