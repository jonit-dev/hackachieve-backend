from django.db import models

# Create your models here.


class Log(models.Model):
    event = models.CharField(max_length=255)
    emitter = models.IntegerField(default=None)
    target = models.IntegerField(default=None)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):  # title on dashboard
        return self.event
