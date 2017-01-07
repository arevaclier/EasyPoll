from django.db import models
# Create your models here.
class Question(models.Model):
    text = models.CharField(max_length=255)
    published_date = models.DateTimeField("Published date")

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.text