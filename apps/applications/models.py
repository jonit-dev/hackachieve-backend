from django.db import models
from apps.properties.models import Property
from apps.resumes.models import Resume


class Application(models.Model):
    resume = models.ManyToManyField(Resume)
    property = models.ManyToManyField(Property)
    timestamp = models.DateTimeField(auto_now_add=True)

    @classmethod
    def apply(cls, resume, property):
        application = Application()
        application.save()

        application.resume.add(resume)
        application.property.add(property)
