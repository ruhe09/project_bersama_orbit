from django.db import models

# Create your models here.
class Posting(models.Model):
    title_text = models.CharField(max_length=30)
    description_text = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=9,decimal_places=0)
    post_text = models.TextField()
    post_image = models.ImageField(upload_to="static")
    pub_date = models.DateTimeField('date published')
    question_text = models.CharField(max_length=200)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.title_text


class Choice(models.Model):
    question = models.ForeignKey(Posting, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)