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
import re

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
        """Only get items already published."""
        now=timezone.now()
        return self.filter(publish_date__lte=now)


    # def has_parents(self):    # todo: rename to "get_post_responses" ?
    #     """Get posts which are a response (ie have a parent post)"""
    #     return self.exclude(parent_post=None)
    #
    #
    # def has_responses(self):    # todo: rename to "get_post_responses" ?
    #     """Get direct responses to the current post"""
    #     for parent in self:
    #         if parent.responses() == False:
    #             self.exclude(parent)
    #     return self


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
        # Get all posts that are not deleted
        qs = PostQuerySet(self.model, using=self._db).exclude(is_deleted=True)

        # Get deleted posts only if they have undeleted responses
           # Get undeleted children with parents
        posts_with_parents_qs = PostQuerySet(self.model, using=self._db).exclude(parent_post=None).exclude(is_deleted=True)
           # Deleted Posts: Get list of ids of parent posts
        set_of_parent_ids = set(posts_with_parents_qs.values_list("parent_post"))
        cleaned_parent_ids_str = re.sub(r'[(),]', r'', str(set_of_parent_ids)[1:-1])
        parent_ids_list = list(map(int, cleaned_parent_ids_str.split()))
           # returns deleted posts only if they have undeleted children
        qs_deleted_parents = PostQuerySet(self.model, using=self._db).filter(is_deleted=True).filter(pk__in=parent_ids_list)#.has_responses()

        return qs | qs_deleted_parents


    def published(self):
        """Filter for published items."""
        return self.get_queryset().published()

    def search_published(self, query=None):
        """
        Take a query and user run a multi-filter search against it on every post by that user,
        including drafts and unpublished items.
         """
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)

    def search_user(self, user, query=None):
        """
        Take a query and user run a multi-filter search against it on every post by that user,
        including drafts and unpublished items.
         """
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().search(query).filter(user=user)


# Todo: get children for topic post and count

class Post(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField()
    slug = models.SlugField(unique=True, max_length=255) #AutoSlugField(populate_from='title', editable=True, unique=True, max_length=255)#default=create_slug(self.title)) # default=slugify(title)
    slug_alias = models.SlugField(unique=True, max_length=255, blank=True, null=True)  #Todo: validation requirements for this (and slug) field itself against each other and admin portal: https://docs.djangoproject.com/en/5.0/howto/custom-model-fields/#converting-values-to-python-objects
    content = MarkdownField(rendered_field='content_rendered', validator=VALIDATOR_CLASSY, use_editor=True, use_admin_editor=True, null=True, blank=True)
    content_rendered = RenderedMarkdownField()
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    parent_post = models.ForeignKey("Post", null=True, blank=True, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)

    def responses(self):    # todo: rename to "get_post_responses" ?
        """Get direct responses to the current post"""
        #return Post.objects.filter(parent_post=self.pk)
        return Post.objects.get(id=self.pk).post_set.all()

    # not in use so far
    # def get_all_children(self, responses_recursive=[]):    # todo: rename to "get_post_responses" ?
    #     """Get all children (responses and responses to responses) recursively from the current post"""
    #
    #     # while self.responses() != None
    #     for response in self.responses():
    #         responses_recursive.append(response)
    #         response.get_all_children(responses_recursive)
    #     return responses_recursive

    def get_parents_to_root_post(self):
        parent_chain = []
        while self.parent_post != None:
            parent_chain.append(self.parent_post)
            self = self.parent_post
        return parent_chain

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
        ordering = ['-updated', '-publish_date','-created']
    def get_absolute_url(self):
        return f"{reverse('posts_index')}{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"

    def get_post_response_create_url(self):
        return f"{self.get_absolute_url()}/post-new/"
