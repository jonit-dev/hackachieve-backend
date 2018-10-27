from django.db import models
from apps.properties.models import Property
from apps.users.models import User


class Application(models.Model):
    tenant = models.ManyToManyField(User)
    property = models.ManyToManyField(Property)

    @classmethod
    def apply(cls, tenant, property):


        application = Application()
        application.save()

        application.tenant.add(tenant)
        application.property.add(property)
