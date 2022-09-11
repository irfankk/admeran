from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tags(models.Model):
    title = models.CharField(max_length=125)
    description = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Snippet(models.Model):
    title = models.CharField(max_length=125)
    content = models.CharField(max_length=125)
    created = models.DateTimeField('date created')
    updated = models.DateTimeField('date updated')
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name="tag_snippets")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_snippets")




