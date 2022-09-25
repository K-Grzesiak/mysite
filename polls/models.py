import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


# Create your models here.

# model to wzorzec - trzeba je zainicjować


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return f"{self.question_text} ---> ID: {self.id}"

    @admin.display(
        boolean=True,
        # ordering="pub_date",
        # ordering="id",
        description="Published recently?",
    )
    # gdy odpytuje o question to zwraca Question (nazwę)
    # def __str__(self):
    #     return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=9) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # gdy odpytuje o Choice to zwraca Choice (nazwę)
    def __str__(self):
        return self.choice_text
