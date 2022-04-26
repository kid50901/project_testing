from django.db import models

# Create your models here.
class assets(models.Model):
    owner=models.CharField(max_length=100, null=False)
    date=models.DateField(null=False)
    assets_debt=models.CharField(max_length=100, null=False)
    account_type=models.CharField(max_length=100, null=False)
    account=models.CharField(max_length=100, null=False)
    TWD_exchange=models.FloatField(null=True,blank=True)
    assets_QTY=models.IntegerField(null=True)
    def __int__(self):
        return self.account_type
class debt(models.Model):
    owner=models.CharField(max_length=100, null=False)
    date=models.DateField(null=False)
    assets_debt=models.CharField(max_length=100, null=False)
    account_type=models.CharField(max_length=100, null=False)
    account=models.CharField(max_length=100, null=False)
    TWD_exchange=models.FloatField(null=True,blank=True)
    debt_QTY=models.IntegerField(null=True)
    def __int__(self):
        return self.account_type
class income(models.Model):
    owner=models.CharField(max_length=100, null=False)
    date=models.DateField(null=False)
    income_type=models.CharField(max_length=100, null=False)
    TWD_exchange=models.FloatField(null=True,blank=True)
    income_QTY=models.IntegerField(null=True)
    def __int__(self):
        return self.account_type

class bigexpend(models.Model):
    owner=models.CharField(max_length=100, null=False)
    date=models.DateField(null=False)
    bigexpend_type=models.CharField(max_length=100, null=False)
    account=models.CharField(max_length=100, null=False)
    bigexpend_QTY=models.IntegerField(null=True)
    def __int__(self):
        return self.bigexpend_type

class expend(models.Model):
    owner=models.CharField(max_length=100, null=False)

    date=models.DateField(null=False)
    expend_type=models.CharField(max_length=100, null=False)
    account=models.CharField(max_length=100, null=False)
    expend_QTY=models.IntegerField(null=True)
    def __int__(self):
        return self.expend_type

class endMeets(models.Model):
    owner=models.CharField(max_length=100, null=False)
    Y=models.IntegerField(null=True)
    M=models.IntegerField(null=True)
    year_month=models.DateField(null=False)
    assets_TWD=models.FloatField(null=True,blank=True)
    debt_TWD=models.FloatField(null=True,blank=True)
    income_TWD=models.FloatField(null=True,blank=True)
    expend_TWD=models.FloatField(null=True,blank=True)
    end_meets=models.FloatField(null=True,blank=True)
    def __int__(self):
        return self.M