from django.db import models

# Create your models here.
from apps.neighborhoods.models import Neighborhood
from apps.users.models import User


class Neighborhood_tenant(models.Model):
    tenant = models.ManyToManyField(User)
    neighborhood = models.ManyToManyField(Neighborhood)

    @classmethod
    def attach(cls, neighborhood, tenant):
        neighborhood_tenant = Neighborhood_tenant()
        neighborhood_tenant.save()
        neighborhood_tenant.tenant.add(tenant)
        neighborhood_tenant.neighborhood.add(neighborhood)
