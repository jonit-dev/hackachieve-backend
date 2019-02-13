from django.db import models

# Create your models here.
from apps.columns.models import Column
from apps.users_categories.models import User_Category


class Column_category(models.Model):
    column = models.ManyToManyField(Column)
    category = models.ManyToManyField(User_Category)

    @classmethod
    def attach(cls, column, category):
        application = Column_category()
        application.save()

        application.column.add(column)
        application.category.add(category)
