from django.db import models
# Create your models here.
class Question(models.Model):
    q_text = models.CharField(max_length=255)
    published_date = models.DateTimeField("Published date")

    def __str__(self):
        return self.q_text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    a_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.a_text