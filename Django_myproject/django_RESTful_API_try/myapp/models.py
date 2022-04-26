from django.db import models

# Create your models here.
class Music(models.Model):
    name = models.CharField(max_length=50)  # 歌曲名稱
    artist = models.CharField(max_length=50)  # 歌手
    album = models.CharField(max_length=50)  # 專輯
    release_date = models.DateField()  # 發行日期