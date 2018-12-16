from django.db import models

# Create your models here.


class Log(models.Model):
    event = models.CharField(max_length=255)
    emitter = models.IntegerField(default=None,null=True)
    target = models.IntegerField(default=None, null=True)
    value = models.CharField(max_length=255,default=None, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):  # title on dashboard
        return self.event
