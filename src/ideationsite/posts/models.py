from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from datetime import datetime as dt
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_CLASSY

User = settings.AUTH_USER_MODEL
# Create your models here.

# class Author(models.Model):
#     username = models.TextField()
#     about = models.TextField() # Todo: add markdown support
#     joined_date = models.DateTimeField("date joined")
#     first_post_date = models.DateTimeField("been posting since") #Todo: "been posting since" or "first posted on" or "date of first post" date? maybe in view
#     #number_of_posts = models.IntegerField(Post.id.latest) #Todo: Foo.objects.latest('id')

class PostQuerySet(models.QuerySet):
    def published(self):
        now=timezone.now()
        return self.filter(publish_date__lte=now)

    def search(self, query):        # Todo: check works with markdown addition
        lookup = (
                    Q(title__icontains=query) |
                    Q(content__icontains=query) |
                    Q(slug__icontains=query) |
                    Q(user__first_name__icontains=query) |
                    Q(user__username__icontains=query)
        )
        return self.filter(lookup)

    #datetimes(field_name, kind, order='ASC', tzinfo=None, is_dst=None)¶

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def search(self, query=None):
        if query is None:
            return self.get_queryset().none()
        return self.get_queryset().published().search(query)    #only search published


class Post(models.Model):                                                           # Todo: a different on-delete or different user? set a tag?
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL) # Todo: add a warning that deleting an account deletes all posts and recommend to export them first - make this a "delete my account, posts and all my data" option)
    # Todo: add an author which defaults to the user creating the post - if someone leaves they can still be credited as author/we can still search it even if they delete their user or hide their contributions or attribution
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    title = models.CharField()
    slug = models.SlugField(unique=True)
    content = MarkdownField(rendered_field='content_rendered', validator=VALIDATOR_CLASSY, use_editor=True, use_admin_editor=True, null=True, blank=True)
    content_rendered = RenderedMarkdownField()
    # Todo: Markdown 1) add visual editor library/tool, 2) enable iframes etc with custom markdown - does this require using a custom validator?

    # pub_date = models.DateTimeField(default=timezone.now, blank=True) #(auto_now_add=True, blank=True) Todo: this seems preferred - would like it to be uneditable in admin, maybe
    publish_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True) #(auto_now_add=True, blank=True) Todo: this seems preferred - would like it to be uneditable in admin, maybe
    created = models.DateTimeField(auto_now_add=True) #(auto_now_add=True, blank=True) Todo: this seems preferred - would like it to be uneditable in admin, maybe
    updated = models.DateTimeField(auto_now=True) #(auto_now_add=True, blank=True) Todo: this seems preferred - would like it to be uneditable in admin, maybe

    @property
    def updated_to_minute(self):
        return self.updated.replace(second=0, microsecond=0)

    @property
    def created_to_minute(self):
        return self.created.replace(second=0, microsecond=0)

    @property
    def published_to_minute(self):
        return self.publish_date.replace(second=0, microsecond=0)

    # updated_to_minute = models.DateTimeField(default=updated.replace(second=0, microsecond=0))
    # created_to_minute = models.DateTimeField(default=created.replace(second=0, microsecond=0))
    # published_to_minute = models.DateTimeField(default=publish_date.replace(second=0, microsecond=0))

                                                            # Todo: add storage for user images etc?
    objects=PostManager()

    class Meta:
        ordering = ['-updated','-publish_date','-created']
    def get_absolute_url(self):
        return f"{reverse('posts_index')}{self.slug}"

    def get_edit_url(self):
        return f"{self.get_absolute_url()}/edit"

    def get_delete_url(self):
        return f"{self.get_absolute_url()}/delete"
