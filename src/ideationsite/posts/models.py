from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from datetime import datetime as dt
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_CLASSY
#from autoslug import AutoSlugField
#from django.utils.text import slugify

User = settings.AUTH_USER_MODEL
# Create your models here.

# class Author(models.Model):
#     username = models.TextField()
#     about = models.TextField()
#     joined_date = models.DateTimeField("date joined")
#     first_post_date = models.DateTimeField("been posting since")
#     #number_of_posts = models.IntegerField(Post.id.latest)

class PostQuerySet(models.QuerySet):
    def published(self):
        now=timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):
        lookup = (
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__username__icontains=query)
        )
        return self.filter(lookup)                                                          #datetimes(field_name, kind, order='ASC', tzinfo=None, is_dst=None)¶

# Topic (Root) posts only
    def topic_posts(self):
        return self.filter(parent_post=None)

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)    #only search published

    def topic_posts(self):
        return self.get_queryset()


# Todo: get children for topic post and count

class Post(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField()
    slug = models.SlugField(unique=True, max_length=255) #AutoSlugField(populate_from='title', editable=True, unique=True, max_length=255)#default=create_slug(self.title)) # default=slugify(title)
    content = MarkdownField(rendered_field='content_rendered', validator=VALIDATOR_CLASSY, use_editor=True, use_admin_editor=True, null=True, blank=True)
    content_rendered = RenderedMarkdownField()
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent_post = models.ForeignKey("Post", null=True, blank=True, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)


    @property
    def updated_to_minute(self):
        return self.updated.replace(second=0, microsecond=0)

    @property
    def created_to_minute(self):
        return self.created.replace(second=0, microsecond=0)

    @property
    def published_to_minute(self):
        return self.publish_date.replace(second=0, microsecond=0)

    objects=PostManager()

    class Meta:
        ordering = ['-publish_date','-updated','-created']
    def get_absolute_url(self):
        return f"{reverse('posts_index')}{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"

    def get_post_response_create_url(self):
        return f"{self.get_absolute_url()}/post-new/"
