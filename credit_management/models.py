import datetime

from django.db import models
from accounts.models import User


#every user can have multiple credit cards
class Credit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    date_created = models.DateField(default=datetime.date.today())

class Transaction(models.Model):

    #Which credit in sending money.
    init_credit = models.PositiveSmallIntegerField(default=0)

    #Credits those are in transaction.
    credits = models.ManyToManyField(Credit)
    money = models.IntegerField(default=0)

    #Transaction with failed status soesn't change balance.
    status = models.CharField(max_length=2, choices={
        ('S', 'Successful'),
        ('F', 'Failed')
    })
    category = models.CharField(max_length=2, choices={
        ('g', 'groceries'),
        ('u', 'utilities')
    })
    date = models.DateField(default=datetime.date.today())
