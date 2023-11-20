from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL
# Create your models here.

# class Author(models.Model):
#     username = models.TextField()
#     about = models.TextField() # Todo: add markdown support
#     joined_date = models.DateTimeField("date joined")
#     first_post_date = models.DateTimeField("been posting since") #Todo: "been posting since" or "first posted on" or "date of first post" date? maybe in view
#     #number_of_posts = models.IntegerField(Post.id.latest) #Todo: Foo.objects.latest('id')

class Post(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL) # Todo: add a warning that deleting an account deletes all posts and recommend to export them first - make this a "delete my account, posts and all my data" option)
    title = models.CharField()
    slug = models.SlugField(unique=True)
    content = models.TextField(null=True, blank=True)   # Todo: add markdown support (incl for title)
    pub_date = models.DateTimeField(default=timezone.now, blank=True) #(auto_now_add=True, blank=True) Todo: this seems preferred - would like it to be uneditable in admin, maybe
                                                            # Todo: add storage for user images etc?

