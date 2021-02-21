from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager




"""class Category(models.Model):
    nameTag = models.CharField(max_length=200)

    def __str__(self):
        return self.nameTag

    def get_absolute_url(self):
        return reverse('post_list')"""


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    #category = models.ManyToManyField(Category)
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title + '|' + str(self.author_id)

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))

    def number_of_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, default='anonymous')
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
