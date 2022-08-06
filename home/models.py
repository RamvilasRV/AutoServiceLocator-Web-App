from django.db import models

# Create your models here.
class data(models.Model):
    location = models.CharField(max_length=250)
    detail1 = models.CharField(max_length=250)
    detail2 = models.CharField(max_length=250)
    detail4 = models.CharField(max_length=250)
    detail3 = models.CharField(max_length=250)
    detail5 = models.CharField(max_length=250)
    
    def __str__(self):
        return self.location + self.detail1 + self.detail2 + self.detail3 + self.detail4 + self.detail5
