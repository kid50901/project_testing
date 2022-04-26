from django.db import models

# Create your models here.
class covid7dayInfo(models.Model):
    location=models.CharField(max_length=100, null=False)
    date=models.DateField(null=False)
    total_cases=models.IntegerField(null=True)
    new_cases=models.IntegerField(null=True)
    total_deaths=models.IntegerField(null=True)
    new_deaths=models.IntegerField(null=True)
    total_vaccinations=models.IntegerField(null=True)
    people_vaccinated=models.IntegerField(null=True)
    people_fully_vaccinated=models.IntegerField(null=True)
    new_vaccinations=models.IntegerField(null=True)
    total_vaccinations_per_hundred=models.IntegerField(null=True)
    people_vaccinated_per_hundred=models.IntegerField(null=True)
    #new_vaccinations=models.IntegerField(null=True)
    Chinese_name=models.CharField(max_length=100,null=True)
    date_str=models.CharField(max_length=100,null=True)
    def __int__(self):
        return self.DR_NO