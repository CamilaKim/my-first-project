from django.db import models
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Asin(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Review(models.Model):
    # RATING_CHOICES = (
    #     (1, '1'),
    #     (2, '2'),
    #     (3, '3'),
    #     (4, '4'),
    #     (5, '5'),
    # )

    asin = models.ForeignKey(Asin, on_delete=models.CASCADE, db_index=True)
    page_number = models.IntegerField(db_index=True)
    review_text = models.CharField(max_length=500, db_index=True)
    pub_date = models.DateTimeField('date published', db_index=True)
    review_header = models.CharField(max_length=200, db_index=True)
    # review_rating = models.IntegerField(choices=RATING_CHOICES, db_index=True)
    review_rating = models.CharField(max_length=200, db_index=True)
    review_author = models.CharField(max_length=200, db_index=True)

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes=models.ManyToManyField(User,related_name='likes')
    text = models.TextField()
    # Time is a rhinocerous
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    @property
    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['created']
    def __unicode__(self):
        return self.text+' - '+self.author.username

