# import json
from tinymce.models import HTMLField
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.forms import model_to_dict
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from AnDjo.settings import STATIC_URL, MEDIA_URL

User = get_user_model()

# Create your models here.

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username   

class Category(models.Model):
    categoria = models.CharField(max_length=100, unique=True, verbose_name='Categoria')

    def __str__(self):
        return self.categoria

    def get_absolute_url(self):
        return reverse("category/")

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Título', unique=True)
    overview = HTMLField(max_length=200, verbose_name='Descripción')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField(verbose_name='Contenido')
    # comment_count = models.IntegerField(default=0)
    # view_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = ProcessedImageField(processors=[ResizeToFill(640, 450)],
                                    format='JPEG',
                                    options={'quality': 60},
                                    verbose_name='Imagen')
    categories = models.ManyToManyField(Category, )
    featured = models.BooleanField(verbose_name='Destacado')
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("post_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("post_delete", kwargs={"pk": self.pk})

    def toJSON(self):
        item = model_to_dict(self, exclude=['next_post', 'previous_post'])
        item['timestamp'] = self.timestamp.strftime('%d-%m-%Y %H:%M %p')
        item['author'] = self.author.user.username
        item['thumbnail'] = '{}{}'.format(MEDIA_URL, self.thumbnail)
        if self.next_post:
           item['next_post'] = self.next_post.title
        if self.previous_post:
           item['previous_post'] = self.previous_post.title
        item['categories'] = [{'name': i.categoria} for i in self.categories.all()]
        return item

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()
    