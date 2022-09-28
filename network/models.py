from tkinter.tix import Tree
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    followers = models.ManyToManyField('self', symmetrical=False, related_name= "following",
                blank=True)
    def count_followers(self):
        return self.followers.count()    
    def count_following(self):
        return User.objects.filter(followers=self).count()
   
class Post(models.Model):
     post_id = models.AutoField(primary_key=True)
     postNote = models.TextField()
     poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", null = True)
     timeStamp = models.DateTimeField(auto_now_add=True, null=True)
     likes = models.IntegerField(default = 0, null=True)
     likers =  models.ManyToManyField(User,  related_name="likerz", null = True)

     def serialize(self):
        return {
            "postNote" : self.postNote,
            "timeStamp" : self.timestamp,
            "likes" : self.likes
        }
   

